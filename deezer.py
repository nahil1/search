import configparser
import os
from subprocess import call
import threading

import requests


def search(search_type, search_term):
    url = "https://api.deezer.com/search/{}?q={}".format(search_type, search_term)
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
    
    with open('config.ini', 'w+') as configfile:  # save
        config.write(configfile)


def get_settings():
    config = _get_config()
    path = config.get('SETTINGS', 'path')
    command = config.get('SETTINGS', 'command')
    websettings = config.get('SETTINGS', 'websettings')

    return path, command, websettings


def set_settings(path, command, websettings):
    config = _get_config()
    config['SETTINGS']['path'] = path
    config['SETTINGS']['command'] = command
    config['SETTINGS']['websettings'] = websettings

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
        call([command.format(path=path, type=media_type, id=id)], 
shell=True)
    except Exception as e:
        print(e)
    return 
    


if __name__ == "__main__":
    print(get_settings())
