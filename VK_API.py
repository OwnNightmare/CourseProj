import requests
from pprint import pprint
import json


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

    def dump(self):
        if self.response:
            with open('note.json', mode='w') as f:
                json.dump(self.response, f, ensure_ascii=False, indent=2)

    def take_photo_url(self):
        if self.response != {}:
            max_resolution = 0
            photo_sizes_list = (self.response['response']['items'][0]['sizes'])
            items = self.response['response']['items']
            for item in items:
                for photo_data in item['sizes']:
                    if photo_data.get('height') + photo_data.get('width') > max_resolution:
                        photo_url = photo_data.get('url')
                        max_resolution = photo_data.get('height') + photo_data.get('width')
            return photo_url
        else:
            return 'Возможно, метод photos.get не был применен'

