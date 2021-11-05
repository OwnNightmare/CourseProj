import requests
from pprint import pprint
import json
import operator

class VkQuery:
    def __init__(self, token, page_id):
        self.token = token
        self.page_id = page_id
        self.version = '5.131.'
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
                print('ssoosso')
        else:
            print('Не получен от ВК АPI')
            return False

    def define_photo_numbers(self, quantity=5):
        common_store = self.store_pictures()
        if common_store:
            common_store.sort(key=operator.itemgetter('pixels'), reverse=True)
            if quantity <= len(common_store):
                return common_store[0:quantity]
            else:
                return common_store


