import configparser, os
from subprocess import call

import requests


def search_album(search_term):
    url = "https://api.deezer.com/search/album?q={}".format(search_term)
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
    
    with open('config.ini', 'w+') as configfile:  # save
        config.write(configfile)


def get_settings():
    config = _get_config()
    path = config.get('SETTINGS', 'path')
    command = config['SETTINGS']['command']

    return path, command


def set_settings(path, command):
    config = _get_config()
    config['SETTINGS']['path'] = path
    config['SETTINGS']['command'] = command

    with open('config.ini', 'w+') as configfile:  # save
        config.write(configfile)


def execute(id):
    path, command = get_settings()
    if path != 'None':
        print(command.format(path=path, id=id))
        call([command.format(path=path, id=id)], shell=True)
        return 'success'
    else:
        return 'no setup'
        
if __name__ == "__main__":
	print(get_settings())
