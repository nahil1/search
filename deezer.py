import configparser
import os
import threading
from subprocess import call

import requests

class NoPathError(Exception):
    pass

def search(search_type, search_term):
    url = "https://api.deezer.com/search/{}?q={}".format(search_type, search_term)
    return _api_call(url)


def get_tracks(type, id):
    url = "https://api.deezer.com/{type}/{id}/tracks".format(type=type, id=id)
    return _api_call(url)


def progress_check():
    file_name, = get_settings('progress_file')
    if not file_name:
        raise NoPathError
    names = []
    with open(file_name, 'r+') as file:
        data = file.readlines()
    if data:
        with open(file_name, 'w'): pass
        for line in data:
            name = line
            media_type, id = line.split('/')[3:5]
            id = id.strip('\n')
            if media_type in ['track', 'album', 'playlsit']:
                name = _api_call('https://api.deezer.com/{}/{}'.format(media_type, id))['title']
            elif type == 'artist':
                name = _api_call('https://api.deezer.com/{}/{}'.format(media_type, id))['name']
            names.append(name)
    return names


def _api_call(url):
    data = requests.get(url)
    if data.status_code == requests.codes.ok:
        try:
            data = data.json()
            if 'data' in data.keys():
                return data['data']
            else:
                return data
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


def get_settings(*settings):
    config = _get_config()
    values = []
    for setting in settings:
        values.append(config.get('SETTINGS', setting, fallback=None))
        
    return values


def set_settings(**settings):
    config = _get_config()
    for key in settings.keys():
        print(key)
        config['SETTINGS'][key] = settings[key]

    with open('config.ini', 'w+') as configfile:  # save
        config.write(configfile)


def execute(media_type, id):
    path, command = get_settings('path', 'command')
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
    a, = get_settings('path')
    print(a)
    
    b, = get_settings('banana')
    print(b)
    
    c = get_settings('path', 'banana')
    print(c)
