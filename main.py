from Yandex_module import YandexClient
from VK_module import VkClient
from tqdm import tqdm
from time import sleep
from pprint import pprint


def taking_user():
    """"Принимает от юзера и возвращает id-VK страницы и токен Я.Диска"""
    vk_id = input('ВК ID: ')
    yandex_token = input('Яндекс Диск токен: ')
    return vk_id, yandex_token


with open('YandexToken.txt', encoding='utf8') as f:
    """Считанный Я.токен используется в тестовом режиме Admin"""
    yan_token = f.read()
with open('VK_id.txt', encoding='utf8') as vk_file:
    vk_serv_key = vk_file.readline().strip()
    vk_token = vk_file.readline().strip()
    pattern_for_vk_query = vk_file.readline()
    my_id = vk_file.readline().strip()


def make_folder(folder_name):
    """ Принимает имя папки, создаёт папку через метод класса, возращает код-ответ"""
    response = (yandex_client.create_folder_on_drive(folder_name))
    return response


def photos_get(owner_id=my_id):
    """Принимает vk id, формирует одноименный запрос к VK API"""
    params = f'owner_id={owner_id}&album_id=profile&extended=1'
    resp = vk_client.make_query('photos.get', params)
    return resp.json()


def upload_and_dump(data):
    """Принимает название папки на Я.Диске, если папка создана(код 201) загружает в нее фото,
    выгружает описание загруженных фото в files_description.json"""

    print('Создаем папку, куда будут загружены все фото(по умолчанию будет создана в корне Я.Диска)')
    resp_folder = 0
    response_photo = 0
    folder_name = 'VK_photos'
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
    for pic_data in tqdm(data, desc='Загрузка на Я.Диск'):
        response_photo = yandex_client.upload_from_url(f'{folder_name}/{pic_data.get("likes")}.png', pic_data.get('url'))
        sleep(.05)
        if response_photo.status_code == 202:
            dumping_data.append({'file_name': f"{pic_data.get('likes')}.png",
                                 'size': pic_data.get('size')
                                 })
            vk_client.dump('files_description.json', dumping_data)
    return response_photo.status_code


def runner(vk_id):
    """Принимает id юзера VK, получает фото профиля, если выбрано 'все' - сохраняет каждое фото макс разрешения,
    загружает на диск, если 'задать' - сортирует по размеру и загружает заданное кол-во фото"""

    photos_get(owner_id=vk_id)
    photo_store = vk_client.store_pictures()
    sorted_photos = []
    if photo_store:
        print('Фото ВК профиля получены')
        mode = input('Загрузить все доступные фото("все") ---- Задать количество вручную("задать"): ').lower()
        if mode == 'все':
            (upload_and_dump(photo_store))
        elif mode == 'задать':
            try:
                quantity = int(input(f'Количество загружаемых фото({len(photo_store)} - max): '))
            except ValueError:
                print('Заданное значение не является числом')
            else:
                sorted_photos = vk_client.define_photo_numbers(photo_store=photo_store, quantity=quantity)
        else:
            sorted_photos = vk_client.define_photo_numbers(photo_store=photo_store)
        if sorted_photos:
            (upload_and_dump(sorted_photos))


def users_get(user_ids):
    """Принимает ВК-id от юзера(только один),  выполняет запрос users.get, возращает ответ в json"""
    method_name = 'users.get'
    response = vk_client.make_query(method_name, f'user_ids={user_ids}')
    return response.json()


def get_true_id(users_data):
    """Принимает резульат запроса users.get, возвращает реальный(числовой) id юзера"""
    true_id = users_data['response'][0].get('id')
    return true_id


if __name__ == '__main__':
    """Admin - тестовый режим с default данными для проверки функциональности"""
    author = 'some person'
    while author not in ['admin', 'user', 'exit']:
        author = input('Admin or User: ').lower().strip()
    if author == 'user':
        user_vk_id, user_yandex_token = taking_user()
        yandex_client = YandexClient(token=user_yandex_token)
        vk_client = VkClient(token=vk_serv_key)
        user_data = (users_get(user_ids=user_vk_id))
        user_vk_id = get_true_id(user_data)
        runner(user_vk_id)
    elif author == 'admin':
        yandex_client = YandexClient(yan_token)
        vk_client = VkClient(vk_serv_key)
        (runner(my_id))
