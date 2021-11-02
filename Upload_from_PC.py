import requests
from pprint import pprint


def get_upload_link(self, path_on_drive):
    url = self.upload_url
    params = {'path': path_on_drive, 'overwrite': True}
    headers = self.get_headers()
    response = requests.get(url=url, params=params, headers=headers).json()
    pprint(response)
    return response
