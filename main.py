import time
from Yandex_module import YandexLoader
from VK_module import VkQuery
from tqdm import tqdm
import tkinter as tk
import tkinter.ttk as ttk
from time import sleep
from pprint import pprint
import urllib.request


def taking_user():
    _vk_id = input('ВК ID: ')
    _yandex_token = input('Яндекс Диск токен: ')
    return _vk_id, _yandex_token


with open('YandexToken.txt', encoding='utf8') as f:
    yan_token = f.read()
with open('VK_id.txt', encoding='utf8') as vk_file:
    vk_token = vk_file.readline().strip()
    pattern_for_vk_query = vk_file.readline()
    my_id = vk_file.readline().strip()
    vk_serv_key = vk_file.readline().strip()


def get_request(method='photos.get', params='default&params', owner_id=my_id):
    if params == 'default&params' and method == 'photos.get':
        params = f'owner_id={owner_id}&album_id=profile&extended=1'
        resp = vk_client.make_query('photos.get', params)
    else:
        resp = vk_client.make_query(method, params)
    return resp.json()


def upload_and_dump(data):
    response = 'response code'
    dumping_data = []
    for pic_data in data:
        response = yandex_client.upload_from_url(f'VK/{pic_data.get("likes")}.png', pic_data.get('url'))
        sleep(.01)
        if response.status_code == 202:
            dumping_data.append({'file_name': f"{pic_data.get('likes')}.png",
                                 'size': pic_data.get('size')
                                 })
            vk_client.dump('files_description.json', dumping_data)
    return response.status_code


def get_and_upload_photos(vk_id=my_id):
    get_request(owner_id=vk_id)
    store = vk_client.store_pictures()
    if store:
        mode = input('Скачать все доступные фото("все") ---- Задать количество вручную("задать")').lower()
        if mode == 'все':
            print(upload_and_dump(store))
        elif mode == 'задать':
            quantity = int(input(f'Количество загружаемых фото({len(store)} - max): '))
            photos = vk_client.define_photo_numbers(quantity)
            if photos:
                print(upload_and_dump(photos))


def users_get():
    method_name = 'users.get'
    response = vk_client.make_query(method_name, f'user_ids={my_id},{161370588}, {97799937}')
    return response


def make_folder():
    response = (yandex_client.create_folder_on_drive('VK'))


if __name__ == '__main__':
    way = input('New or Old: ').lower()
    if way == 'new':
        user_vk_id, user_yandex_token = taking_user()
        yandex_client = YandexLoader(yan_token)
        vk_client = VkQuery(vk_serv_key, user_vk_id)
        make_folder()
        get_and_upload_photos(user_vk_id)
    else:
        yandex_client = YandexLoader(yan_token)
        vk_client = VkQuery(vk_serv_key, my_id)
        get_and_upload_photos()
