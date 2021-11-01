from MyUploader import MyUploader

with open('YandexToken.txt', encoding='utf8') as f:
    yan_token = f.read()

yan_loader = MyUploader(yan_token)


def upload():
    yan_loader.upload_file_to_ya_drive('Education/xxx', r'C:\Users\yurab\Git\Another dev.txt')


def make_folder():
    print(yan_loader.create_folder_on_drive('Education/Vk'))
