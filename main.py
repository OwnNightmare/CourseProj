from MyUploader import MyUploader
from VK_API import VkQuery

with open('YandexToken.txt', encoding='utf8') as f:
    yan_token = f.read()
with open('VK_id.txt', encoding='utf8') as vk_file:
    vk_token = vk_file.readline().strip()
    pattern_for_vk_query = vk_file.readline()
    my_id = vk_file.readline().strip()
    vk_serv_key = vk_file.readline().strip()

yan_loader = MyUploader(yan_token)
me = VkQuery(vk_serv_key)
me.make_query('users.get', f'user_ids={my_id},{161370588}')


def upload():
    yan_loader.upload_file_to_ya_drive('Education/xxx', r'C:\Users\yurab\Git\Another dev.txt')


def make_folder():
    print(yan_loader.create_folder_on_drive('Education/Vk'))
