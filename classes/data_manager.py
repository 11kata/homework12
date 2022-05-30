import json
from pprint import pprint as pp

from classes.exceptions import DataSourceBrokenException


class DataManager:

    def __init__(self, path):
        self.path = path  # путь к файлу

    def load_data(self):
        """ Загружает данные из файла другими методами"""
        try:
            with open(self.path, 'r', encoding='utf-8') as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            raise DataSourceBrokenException('Файл поврежден ')
        return data

    def save_data(self, data):
        """ Перезаписывает переданные данные в файл с данными """
        with open(self.path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=2)

    def get_all(self):
        """ Отдает полный список данных"""
        data = self.load_data()
        return data

    def search(self, substring):
        """ Отдает посты, которые содержат substring"""

        posts = self.load_data()
        substring = substring.lower()
        matching_posts = [post for post in posts if substring in post['content'].lower()]
        return matching_posts

    def add(self, post):
        """ Добавляет в хранилище определенный пост"""
        if type(post) != dict:
            raise TypeError('Это не правильный формат поста')

        posts = self.load_data()
        posts.append(post)
        self.save_data(posts)


dm = DataManager('../data/posts.json')
#pp(dm.get_all())
