from MyUploader import MyUploader

with open('YandexToken.txt', encoding='utf8') as f:
    yan_token = f.read()

yan_loader = MyUploader(yan_token)
yan_loader.upload_file_to_ya_drive('Education/xxx', r'C:\Users\yurab\Git\Another dev.txt')
