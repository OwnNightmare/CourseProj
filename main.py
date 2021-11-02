from MyUploader import MyUploader
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
    resp = me.make_query(method_name, f'owner_id={my_id}&album_id=profile')
    me.take_photo_url()
    return resp.json()


def users_get():
    method_name = 'users.get'
    me.make_query(method_name, f'user_ids={my_id},{161370588}, {97799937}')


def upload():
    yan_loader.upload_from_url('Education/Vk/photo.png', me.take_photo_url())


def make_folder():
    print(yan_loader.create_folder_on_drive('Education/Vk'))


if __name__ == '__main__':
    photos_get()
    print('')
    print(me.take_photo_url())
