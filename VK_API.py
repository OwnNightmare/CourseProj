import requests
from pprint import pprint


class VkQuery:
    def __init__(self, token):
        self.token = token
        self.version = '5.131.'
        self.url_main = 'https://api.vk.com/method'

    def make_query(self, method_name, params=''):
        resp = requests.get(f'{self.url_main}/{method_name}?{params}&access_token={self.token}&v={self.version}')
        return resp