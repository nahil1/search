import configparser
import os


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
    config['SETTINGS']['password'] = 'None'

    with open('config.ini', 'w+') as configfile:  # save
        config.write(configfile)


def get_settings(*settings):
    config = _get_config()
    values = []
    for setting in settings:
        values.append(config.get('SETTINGS', setting, fallback=None))
    if len(values) == 1:
        return values[0]

    return values


def set_settings(**settings):
    config = _get_config()
    for key in settings.keys():
        config['SETTINGS'][key] = settings[key]

    with open('config.ini', 'w+') as configfile:  # save
        config.write(configfile)
