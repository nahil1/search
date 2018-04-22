import configparser
import os
import threading
from subprocess import call

import requests


def search(search_type, search_term):
    url = "https://api.deezer.com/search/{}?q={}".format(search_type, search_term)
    return _api_call(url)


def get_tracks(type, id):
    url = "https://api.deezer.com/{type}/{id}/tracks".format(type=type, id=id)
    return _api_call(url)


def progress_check():
    with open('output.txt', 'r+') as file:
        data = file.readlines()
    if data:
        with open('output.txt', 'w'): pass
    return data


def _api_call(url):
    data = requests.get(url)
    if data.status_code == requests.codes.ok:
        try:
            return data.json()['data']
        except ValueError:
            return None
    else:
        return None


def _get_config():
    config = configparser.ConfigParser()
    if not os.path.exists('config.ini'):
        _make_config(config)
    config.read('config.ini')
    return config


def _make_config(config):
    config['SETTINGS'] = {}
    config['SETTINGS']['path'] = 'None'
    config['SETTINGS']['command'] = 'None'
    config['SETTINGS']['websettings'] = 'True'
    config['SETTINGS']['progress_file'] = 'output.txt'
    
    with open('config.ini', 'w+') as configfile:  # save
        config.write(configfile)


def get_settings():
    config = _get_config()
    path = config.get('SETTINGS', 'path')
    command = config.get('SETTINGS', 'command')
    websettings = config.get('SETTINGS', 'websettings')
    progress_file = config.get('SETTINGS', 'progress_file')

    return path, command, websettings, progress_file


def set_settings(path, command, websettings, progress_file):
    config = _get_config()
    config['SETTINGS']['path'] = path
    config['SETTINGS']['command'] = command
    config['SETTINGS']['websettings'] = websettings
    config['SETTINGS']['progress_file'] = progress_file

    with open('config.ini', 'w+') as configfile:  # save
        config.write(configfile)


def execute(media_type, id):
    path, command = get_settings()[0:2]
    if path != 'None':
        t = threading.Thread(target=execute_thread, args=(media_type, id, path, command))
        t.start()
        return 'started'
    else:
        return 'no setup'


def execute_thread(media_type, id, path, command):
    print(command.format(path=path, type=media_type, id=id))
    try:
        call([command.format(path=path, type=media_type, id=id)], shell=True)
    except Exception as e:
        print(e)
    return 


if __name__ == "__main__":
    print(get_settings())
