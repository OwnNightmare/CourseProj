import requests
from pprint import pprint


class MyUploader:
    def __init__(self, token: str):
        self.token = token

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {self.token}'
        }

    def get_upload_link(self, path_on_drive):
        url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        params = {'path': path_on_drive, 'overwrite': True}
        headers = self.get_headers()
        response = requests.get(url=url, params=params, headers=headers).json()
        pprint(response)
        return response

    def upload_file_to_ya_drive(self, path_on_drive: str, file_path: str):
        response = self.get_upload_link(path_on_drive=path_on_drive)
        url = response.get('href')
        up = requests.put(url=url, data=open(file=file_path, mode='rb'))
        print(up.status_code)