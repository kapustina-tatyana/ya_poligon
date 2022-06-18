import os
import requests


class YaUploader:

    host = 'https://cloud-api.yandex.net'

    def __init__(self, token: str):
        self.token = token

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {self.token}'
        }

    def _get_upload_link(self, path):
        """Метод получает ссылку на загружаемый файл"""
        url = f'{self.host}/v1/disk/resources/upload/'
        headers = self.get_headers()
        params = {'path': path, 'overwrite': True}
        response = requests.get(url, params=params, headers=headers)
        resp_status = response.json().get('href')
        return resp_status

    def upload(self, file_path: str):
        """Метод загружает указанный файл на яндекс диск"""
        path = os.path.basename(file_path)
        upload_link = self._get_upload_link(path)
        headers = self.get_headers()
        response = requests.put(upload_link, data=open(file_path, 'rb'), headers=headers)
        response.raise_for_status()
        if response.status_code == 201:
            print('Success')


    def upload_fl(self, file_list: str):
        """Метод загружает файлы по списку file_list на яндекс диск"""
        with open(file_list, 'r') as file:
            for line in file:
                self.upload(line.rstrip())



if __name__ == '__main__':
    # Получить путь к загружаемому файлу и токен от пользователя
    path_to_file = input('Введите абсолютный путь к загружаемому файлу \n или списку загружаемых файлов: ')
    token = input('Введите токен: ')
    yadisk = YaUploader(token)
    uploader = YaUploader(token)
    extension = os.path.splitext(path_to_file)[1]
    if extension == '.txt':
        result = uploader.upload_fl(path_to_file)
    else:
        result = uploader.upload(path_to_file)





