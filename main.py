from Yandex_module import YandexClient
from VK_module import VkClient
from tqdm import tqdm
from time import sleep
from pprint import pprint


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


def make_folder(folder_name):
    response = (yandex_client.create_folder_on_drive(folder_name))
    return response


def photos_get(method='photos.get', params='default&params', owner_id=my_id):
    if params == 'default&params' and method == 'photos.get':
        params = f'owner_id={owner_id}&album_id=profile&extended=1'
        resp = vk_client.make_query('photos.get', params)
    else:
        resp = vk_client.make_query(method, params)
    return resp.json()


def upload_and_dump(data):
    print('Создаем новую папку, куда будут загружены все фото(по умолчанию будет создана в корне Я.Диска)')
    resp_folder = 0
    folder_name = 'VK'
    while resp_folder != 201:
        folder_name = input('Имя папки на Я.Диске: ')
        resp_folder = make_folder(folder_name)
        if resp_folder == 201:
            print(f'Папка {folder_name} успешно создана (код {resp_folder})')
        elif resp_folder == 409:
            print(f'{folder_name} уже существует(код {resp_folder}). Выберите другое имя или путь')
        else:
            print(f'Ошибка. Папка не создана. Код - {resp_folder}')
            return 'operation canceled'
    dumping_data = []
    for pic_data in tqdm(data, desc='Выгрузка'):
        response = yandex_client.upload_from_url(f'{folder_name}/{pic_data.get("likes")}.png', pic_data.get('url'))
        sleep(.05)
        if response.status_code == 202:
            dumping_data.append({'file_name': f"{pic_data.get('likes')}.png",
                                 'size': pic_data.get('size')
                                 })
            vk_client.dump('files_description.json', dumping_data)

    return response.status_code


def runner(vk_id):
    photos_get(owner_id=vk_id)
    photos = ''
    pic_store = vk_client.store_pictures()
    if pic_store:
        print('Фото ВК профиля получены')
        mode = input('Загрузить все доступные фото("все") ---- Задать количество вручную("задать"): ').lower()
        if mode == 'все':
            print(upload_and_dump(pic_store))
        elif mode == 'задать':
            try:
                quantity = int(input(f'Количество загружаемых фото({len(pic_store)} - max): '))
            except ValueError:
                print('Заданное значение не является числом')
            else:
                photos = vk_client.define_photo_numbers(photo_store=pic_store, quantity=quantity)
        else:
            photos = vk_client.define_photo_numbers(photo_store=pic_store)
        if photos:
            print(f'Выгрузка завершена - {upload_and_dump(photos)}')


def users_get():
    method_name = 'users.get'
    response = vk_client.make_query(method_name, f'user_ids={my_id},{161370588}, {97799937}, h0odrich')
    return response


if __name__ == '__main__':
    way = input('Admin or User: ').lower()
    if way == 'user':
        user_vk_id, user_yandex_token = taking_user()
        yandex_client = YandexClient(yan_token)
        vk_client = VkClient(vk_serv_key, user_vk_id)
        runner(user_vk_id)
    else:
        yandex_client = YandexClient(yan_token)
        vk_client = VkClient(vk_serv_key, my_id)
        (runner(my_id))
