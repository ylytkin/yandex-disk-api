from pathlib import Path

import requests

__all__ = [
    'get_file_info',
    'publish_object',
    'publish_object_and_get_link',
    'get_file_list',
    'download_file',
    'upload_file',
    'delete_file',
    'move_file',
]


def get_headers(token: str):
    return {
        'Authorization': f'OAuth {token}',
        'Content-Type': 'application/json',
    }


def get_file_info(path: str, token: str):
    url = 'https://cloud-api.yandex.net/v1/disk/resources'
    params = {'path': path}
    
    r = requests.get(url, params=params, headers=get_headers(token))
    
    return r.json()


def publish_object(path: str, token: str):
    url = 'https://cloud-api.yandex.net/v1/disk/resources/publish'
    params = {'path': path}
    
    r = requests.put(url, params=params, headers=get_headers(token))
    
    return r.json()


def publish_object_and_get_link(path: str, token: str) -> str:
    response = publish_object(path, token=token)
    
    if response.get('error'):
        return
    
    file_info = get_file_info(path, token=token)
    
    return file_info.get('public_url')
    
    
def get_file_list(path: str, token: str, files_only: bool = True):
    url = 'https://cloud-api.yandex.net/v1/disk/resources'
    limit = 20
    offset = 0
    total = None
    
    filelist = []
    
    while total is None or offset < total:
        params = {'path': path, 'limit': limit, 'offset': offset}
        
        try:
            r = requests.get(url, params=params, headers=get_headers(token))
            result = r.json()['_embedded']

            total = result['total']
            offset += limit

            filelist.extend(result['items'])
        
        except Exception as e:
            print(params, e)
            
    if files_only:
        filelist = [file for file in filelist if file['type'] == 'file']
    
    return filelist


def get_file_download_url(fpath: str, token: str) -> str:
    url = 'https://cloud-api.yandex.net/v1/disk/resources/download'
    params = {'path': fpath}

    r = requests.get(url, params=params, headers=get_headers(token))
    
    return r.json()['href']


def download_file(disk_fpath: str, fpath: Path, token: str):
    url = get_file_download_url(disk_fpath, token=token)
    r = requests.get(url, headers=get_headers(token))
    
    with fpath.open('wb') as file:
        file.write(r.content)
        
        
def get_file_upload_url(disk_fpath: str, token: str, overwrite: bool = False) -> str:
    url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
    params = {'path': disk_fpath, 'overwrite': overwrite}
    
    r = requests.get(url, params=params, headers=get_headers(token))
    
    if r.status_code == 409:
        print(r.json()['description'])
    
    else:
        return r.json()['href']

        
def upload_file(fpath: Path, disk_fpath: str, token: str, overwrite: bool = False):
    url = get_file_upload_url(disk_fpath, token=token, overwrite=overwrite)
    
    if url is not None:
        with fpath.open('rb') as file:
            requests.put(url, data=file)
            
        return True
    
    return False


def delete_file(disk_fpath: str, token: str):
    url = 'https://cloud-api.yandex.net/v1/disk/resources'
    params = {'path': disk_fpath}
    
    return requests.delete(url, params=params, headers=get_headers(token))


def move_file(disk_from_fpath: str, disk_to_fpath: str, token: str, overwrite: bool = False):
    url = 'https://cloud-api.yandex.net/v1/disk/resources/move'
    params = {'from': disk_from_fpath, 'path': disk_to_fpath, 'overwrite': overwrite}
    
    r = requests.post(url, params=params, headers=get_headers(token))
    
    if r.status_code == 409:
        print(r.json()['description'])
        
        return False
    
    return True

