"""Веб интерфейс проекта"""

from flask import Flask

import os


# Получаем абсолютный путь к папке модуля
_dir = os.path.dirname(os.path.abspath(__file__))

# Без этого всё ломается, потому что фласк пытается
# искать папку templates в папке проекта а не модуля
template_dir = os.path.join(_dir, 'templates')
static_dir = os.path.join(_dir, 'static')


# Создаём объект приложения
app = Flask('ling',
            template_folder=template_dir,
            static_folder=static_dir)


# Загрузка конфигов, необходимых для компонентов вроде планировщика
from . import config
app.config.from_object(config)


# Импортируем маршрутизацию
from . import routes


# Импортируем и добавляем функции препроцессинга для jinja
from .functions import for_jinja

app.jinja_env.globals.update(**for_jinja)
