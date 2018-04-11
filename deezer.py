import configparser

import requests


def config_section_map(config, section):
    dict1 = {}
    options = config.options(section)
    for option in options:
        try:
            dict1[option] = config.get(section, option)
            if dict1[option] == -1:
                print("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1


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


def execute(url):
    config = configparser.ConfigParser()
    config.read('config.ini')
    path = config_section_map(config, "execute")['path']
    if path != 'None':
        command = config_section_map(config, "execute")['command'].format(path=path, url=url)
        print(command)
        return 'success'
    else:
        return 'no setup'
