import requests
from pprint import pprint
import json
import operator


class VkClient:
    def __init__(self, token, version='5.131.'):
        self.token = token
        self.version = version
        self.url_main = 'https://api.vk.com/method'
        self.response = {}

    def make_query(self, method_name, params=''):
        resp = requests.get(f'{self.url_main}/{method_name}?{params}&access_token={self.token}&v={self.version}')
        self.response = resp.json()
        return resp

    def dump(self, file, data, opening_mode='w'):
        if self.response:
            with open(file=file, mode=opening_mode) as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

    def store_pictures(self):
        if self.response != {}:
            try:
                items = self.response['response']['items']  # Список фото всех размеров,элемент списка - 1 фото в n размерах
                pictures_store = []
                photo_data = {}
                photo_url = 'some url'
                for item in items:   # item - словарь для одного фото с x числом размеров(словарей внутри ключа 'sizes')
                    likes_count = item['likes'].get('count')
                    max_resolution = 0
                    for photo_data in item['sizes']:   # словарь, с данными о каждом размере фото
                        if photo_data.get('height') + photo_data.get('width') > max_resolution:
                            photo_url = photo_data.get('url')
                            max_resolution = photo_data.get('height') + photo_data.get('width')
                    pictures_store.append({'url': photo_url,
                                           'size': f"{photo_data.get('height')}x{photo_data.get('width')}",
                                           'likes': likes_count,
                                           'pixels': photo_data.get('height') + photo_data.get('width')})
                return pictures_store
            except KeyError:
                pprint(self.response)
        else:
            print('Не получен от ВК АPI')
            return False

    def define_photo_numbers(self, photo_store, quantity=5):
        if photo_store:
            photo_store.sort(key=operator.itemgetter('pixels'), reverse=True)
            if quantity <= len(photo_store):
                return photo_store[0:quantity]
            else:
                return photo_store


