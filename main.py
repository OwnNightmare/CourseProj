from Yandex_API import MyUploader
from VK_API import VkQuery
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
me = VkQuery(vk_serv_key)


def photos_get():
    method_name = 'photos.get'
    params = f'owner_id={my_id}&album_id=profile&extended=1'
    resp = me.make_query(method_name, params)
    me.store_pictures()
    return resp.json()


def users_get():
    method_name = 'users.get'
    me.make_query(method_name, f'user_ids={my_id},{161370588}, {97799937}')


def upload():
    pic_pack = me.store_pictures()
    for pic_data in pic_pack:
        for pic_name, pic_url in pic_data.items():
            yan_loader.upload_from_url(f'Education/Vk/{pic_name}.png', pic_url)


def make_folder():
    print(yan_loader.create_folder_on_drive('Education/Vk'))


if __name__ == '__main__':
    photos_get()
    upload()
    print('')


