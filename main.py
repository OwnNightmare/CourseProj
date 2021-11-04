import time
from Yandex_API import MyUploader
from VK_API import VkQuery
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


def making_vk_query(method='photos.get', params='default&params', owner_id=my_id):
    if params == 'default&params' and method == 'photos.get':
        params = f'owner_id={owner_id}&album_id=profile&extended=1'
        resp = vk_client.make_query('photos.get', params)
    else:
        resp = vk_client.make_query(method, params)
    return resp.json()


def users_get():
    method_name = 'users.get'
    vk_client.make_query(method_name, f'user_ids={my_id},{161370588}, {97799937}')


def upload_and_dump():
    response = 'response code'
    dumping_data = []
    pic_pack = vk_client.store_pictures()
    pprint(pic_pack)
    for pic_data in pic_pack:
        response = yandex_client.upload_from_url(f'Education/Vk/{pic_data.get("likes")}.png', pic_data.get('url'))
        sleep(2.0)
        if response.status_code == 202:
            dumping_data.append({'file_name': f"{pic_data.get('likes')}.png",
                                 'size': pic_data.get('size')
                                 })
            vk_client.dump('files_description.json', dumping_data)
    return response.status_code


def get_and_upload_photos(vk_id=my_id):
    making_vk_query(owner_id=vk_id)
    pprint(vk_client.define_photo_numbers())
    # print(upload_and_dump())


def make_folder():
    print(yandex_client.create_folder_on_drive('Education/Vk'))


if __name__ == '__main__':
    way = input('New or Old: ').lower()
    if way == 'new':
        user_vk_id, user_yandex_token = taking_user()
        yandex_client = MyUploader(yan_token)
        vk_client = VkQuery(vk_serv_key, user_vk_id)
        get_and_upload_photos(user_vk_id)
    else:
        yandex_client = MyUploader(yan_token)
        vk_client = VkQuery(vk_serv_key, my_id)
        get_and_upload_photos()



