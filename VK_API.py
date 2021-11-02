import requests
from pprint import pprint


class VkQuery:
    def __init__(self, token):
        self.token = token
        self.version = '5.131.'
        self.url_main = 'https://api.vk.com/method'
        self.response = {}

    def make_query(self, method_name, params=''):
        resp = requests.get(f'{self.url_main}/{method_name}?{params}&access_token={self.token}&v={self.version}')
        self.response = resp.json()
        return resp

    def take_photo_url(self):
        if self.response != {}:
            photo_url = self.response['response']['items'][0]['sizes'][4]['url']
            return photo_url