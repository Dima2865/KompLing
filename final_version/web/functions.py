"""Всякие полезные функции для веб-интерфейса"""

from .constants import *

from db import Article

from datetime import datetime
import pytz

from typing import Iterable


def format_params(**params) -> str:
    """Собирает строку url параметров из переданных аргументов"""

    return '&'.join([f'{n}={v}' for n, v in params.items()])


def make_nav_url(endpoint, page=0, sort=None, order=0, only=None) -> str:
    """
    Создаёт ссылку для перехода на заданную страницу
    списка статей с сохранением сортировки
    """

    params = {'page': page}

    if only:
        params['only'] = only

    if sort:
        params['sort'] = sort
        params['order'] = order or 0

    return endpoint + '?' + format_params(**params)


def format_date(date: datetime,
                timezone: str = DEFAULT_TIMEZONE,
                date_format: str = DATE_FORMAT) -> str:

    """Форматирует дату в заданный формат в заданной часовой зоне"""

    return date.astimezone(pytz.timezone(timezone)).strftime(date_format)


def capitalize(string: str) -> str:
    """Делает первую букву строки большой"""

    return string[:1].upper() + string[1:]


def get_paragraphs(article: Article, sentences: Iterable):
    """Возвращает абзацы статьи, выделяя в них найденные предложения"""

    for paragraph in article.content:
        for sentence in sentences:
            paragraph = paragraph.replace(
                sentence.content,
                f'<span class="sentence-inline {sentence.tonality_class}">'
                f'{sentence.content}'
                f'<a class="sentence-inline-link" href={sentence.url}><i class="fas fa-external-link-alt"></i></a>'
                f'</span>'
            )

        yield paragraph



# Эти функции будут добавлены в функции,
# которые может использовать jinja при процессинге шаблонов
for_jinja = {'make_nav_url': make_nav_url,
             'format_date': format_date,
             'capitalize': capitalize,
             'get_paragraphs': get_paragraphs,
             'ws_name': WEBSITE_NAME,
             'ws_desc': WEBSITE_DESC}
