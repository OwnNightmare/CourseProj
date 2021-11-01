import requests
from pprint import pprint


class MyUploader:
    def __init__(self, token: str):
        self.token = token
        self.common_url = 'https://cloud-api.yandex.net'
        self.create_folder_url = '/v1/disk/resources'

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {self.token}'
        }

    def create_folder_on_drive(self, path_on_drive):
        headers = self.get_headers()
        params = {'path': path_on_drive}
        response = requests.put(url=f'{self.common_url}{self.create_folder_url}', params=params, headers=headers)
        return response

    def get_upload_link(self, path_on_drive):
        url = f'{self.common_url}/v1/disk/resources/upload'
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