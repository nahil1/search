import threading
from subprocess import call
import requests

from config import get_settings


class NoPathError(Exception):
    pass


def search(search_type, search_term):
    url = "https://api.deezer.com/search/{}?q={}".format(search_type, search_term)
    return _api_call(url)


def get_tracks(item_type, item_id, limit=50):
    if item_type == 'artist':
        url = "https://api.deezer.com/artist/{id}/top?limit={limit}".format(limit=limit, id=item_id)
    else:
        url = "https://api.deezer.com/{type}/{id}/tracks".format(type=item_type, id=item_id)
    return _api_call(url)


def progress_check():
    file_name = get_settings('progress_file')
    if not file_name:
        raise NoPathError
    names = []
    with open(file_name, 'r+') as file:
        data = file.readlines()
    if data:
        with open(file_name, 'w'): pass
        for line in data:
            name = line
            media_type, item_id = line.split('/')[3:5]
            item_id = item_id.strip('\n')
            if media_type in ['track', 'album', 'playlsit']:
                name = _api_call('https://api.deezer.com/{}/{}'.format(media_type, item_id))['title']
            elif type == 'artist':
                name = _api_call('https://api.deezer.com/{}/{}'.format(media_type, item_id))['name']
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


def execute(media_type, item_id):
    path, command, quality = get_settings('path', 'command', 'quality')
    if command != 'None':
        t = threading.Thread(target=execute_thread, args=(media_type, item_id, path, command, quality))
        t.start()
        return 'started'
    else:
        return 'no setup'


def execute_thread(media_type, item_id, path, command, quality):
    print(command.format(path=path, type=media_type, id=item_id, quality=quality))
    try:
        call([command.format(path=path, type=media_type, id=item_id, quality=quality)], shell=True)
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
