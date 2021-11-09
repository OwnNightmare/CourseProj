import requests

"""
Классы: YandexClient

Методы: get_headers() -> dict
         create_folder_on_drive(string) -> Response.status_code 
         upload_from_url(str, str) -> Response           
"""


class YandexClient:
    """
    Класс для формирования запросов к REST API Яндекс Диска

    Атрибуты
    -------
    token : str
        Яндекс токен пользователя
    common_url : str
        Предопреленный. Общая часть url пути к API Диска
    create_folder_url : str
        Предопределенный.  Часть url адреса к API Диска для создания папки
    upload_url : str
        Предопределенный. Полный url к API Диска для загрузки файлов по url

    Методы
    ------
    get_headers():
        возвращает заголовки запроса, передает Я.токен в запросе для аутентификации
    create_folder_on_drive(path_on_drive):
        создает папку с именем переданным в path_on_drive
    upload_from_url(path_on_drive, url_path):
        загружает файл на Я.Диск
    """

    def __init__(self, token: str):
        """Устанавливает необходимые атрибуты для объекта YandexClient"""
        self.token = token
        self.common_url = 'https://cloud-api.yandex.net'
        self.create_folder_url = '/v1/disk/resources'
        self.upload_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'

    def get_headers(self):
        """Формирует заголовки запроса"""
        return {
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {self.token}'
        }

    def create_folder_on_drive(self, path_on_drive):
        """Создает папку на Я.Диске"""
        headers = self.get_headers()
        params = {'path': path_on_drive}
        response = requests.put(url=f'{self.common_url}{self.create_folder_url}', params=params, headers=headers)
        return response.status_code

    def upload_from_url(self, path_on_drive: str, url_path: str):
        """Загружает файл в указанную папку(path_on_drive) на Диске, файл находится по url_path"""
        params = {
            'path': {path_on_drive},
            'url': {url_path}
        }
        response = requests.post(self.upload_url, params=params, headers=self.get_headers())
        return response
