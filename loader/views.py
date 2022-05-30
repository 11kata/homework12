import os.path
import random

from flask import Blueprint, render_template, request, current_app

from classes.data_manager import DataManager
from .exceptions import OutOfFreeNamesError, PictureFormatNotSupportedError, PictureNotUploadedError
from .loader_manager import LoaderManager

loader_blueprint = Blueprint('loader_blueprint', __name__, template_folder='templates')


@loader_blueprint.route('/post', methods=['GET'])
def page_form():
    return render_template('post_form.html')


@loader_blueprint.route('/post', methods=['POST'])
def page_create_post():
    # Получаем данные
    picture = request.files.get('picture', None)
    content = request.values.get('content', '')

    # Сохраняем картинку с помощью менеджера загрузки
    loader_manager = LoaderManager()
    filename_saved = loader_manager.save_with_random_name(picture)
    web_path = f'/uploads/images/{filename_saved}'  # получаем путь для браузера

    post = {'pic': web_path, 'content': content}  # Создаем данные для записи в файл
    path = current_app.config.get('POST_PATH')
    data_manager = DataManager(path)
    data_manager.add(post)  # Добавляем данные в файл

    return render_template('post_uploaded.html', pic=web_path, content=content)


@loader_blueprint.errorhandler(OutOfFreeNamesError)
def error(e):
    return 'закончились имена для картинок'


@loader_blueprint.errorhandler(PictureFormatNotSupportedError)
def error(e):
    return 'Формат картинки не поддерживается'


@loader_blueprint.errorhandler(PictureNotUploadedError)
def error(e):
    return 'Что-то пошло не так'
