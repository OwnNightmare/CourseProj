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

    def store_pictures(self):
        if self.response != {}:
            items = self.response['response']['items']  # Список фото всех размеров,элемент списка - 1 фото в n размерах
            pictures_store = []
            photo_url = 'some url'
            for item in items:   # item - словарь для одного фото с x числом размеров(словарей внутри ключа 'sizes')
                likes_count = item['likes'].get('count')
                max_resolution = 0
                for photo_data in item['sizes']:   # словарь, с данными о каждом размере фото
                    if photo_data.get('height') + photo_data.get('width') > max_resolution:
                        photo_url = photo_data.get('url')
                        max_resolution = photo_data.get('height') + photo_data.get('width')
                pictures_store.append({f'{likes_count}': photo_url})
            return pictures_store
        else:
            return 'Возможно, метод photos.get не был применен'

