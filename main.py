import time

from Yandex_API import MyUploader
from VK_API import VkQuery
from tqdm import tqdm
import tkinter as tk
import tkinter.ttk as ttk
from time import sleep
from pprint import pprint
import urllib.request


with open('YandexToken.txt', encoding='utf8') as f:
    yan_token = f.read()
with open('VK_id.txt', encoding='utf8') as vk_file:
    vk_token = vk_file.readline().strip()
    pattern_for_vk_query = vk_file.readline()
    my_id = vk_file.readline().strip()
    vk_serv_key = vk_file.readline().strip()

yan_loader = MyUploader(yan_token)
me = VkQuery(vk_serv_key, my_id)


def making_vk_query(method='photos.get', params='default&params'):
    if params == 'default&params' and method == 'photos.get':
        params = f'owner_id={my_id}&album_id=profile&extended=1'
        resp = me.make_query('photos.get', params)
    else:
        resp = me.make_query(method, params)
    return resp.json()


def users_get():
    method_name = 'users.get'
    me.make_query(method_name, f'user_ids={my_id},{161370588}, {97799937}')


def upload_and_dump():
    response = 'response code'
    dumping_data = []
    pic_pack = me.store_pictures()
    for pic_data in pic_pack:
        response = yan_loader.upload_from_url(f'Education/Vk/{pic_data.get("likes")}.png', pic_data.get('url'))
        sleep(2.0)
        if response.status_code == 202:
            dumping_data.append({'file_name': f"{pic_data.get('likes')}.png",
                                 'size': pic_data.get('size')
                                 })
            me.dump('files_description.json', dumping_data)
    return response.status_code


def get_and_upload_photos():
    making_vk_query()
    print(upload_and_dump())


def make_folder():
    print(yan_loader.create_folder_on_drive('Education/Vk'))


if __name__ == '__main__':
    get_and_upload_photos()


