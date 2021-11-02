import requests
from pprint import pprint
import webbrowser


class MyUploader:
    def __init__(self, token: str):
        self.token = token
        self.common_url = 'https://cloud-api.yandex.net'
        self.create_folder_url = '/v1/disk/resources'
        self.upload_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'

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

    def upload_from_url(self, path_on_drive: str, url_file: str):
        params = {
            'path': {path_on_drive},
            'url': {url_file}
        }
        r = requests.post(self.upload_url, params=params, headers=self.get_headers())
        print(r)

    # def get_upload_link(self, path_on_drive):
    #     url = self.upload_url
    #     params = {'path': path_on_drive, 'overwrite': True}
    #     headers = self.get_headers()
    #     response = requests.get(url=url, params=params, headers=headers).json()
    #     pprint(response)
    #     return response