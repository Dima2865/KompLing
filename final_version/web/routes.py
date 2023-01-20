"""Правила возвращения страниц"""

from . import app
from .constants import *

from flask import render_template, request, jsonify
from db import Article, DEFAULT_DATABASE
from mongoengine import ValidationError, DoesNotExist, connect, disconnect

import math
from datetime import datetime
from traceback import print_exc

from main import run_pars_kol, run_pars_date


@app.context_processor
def add_now():
    return {'now': datetime.now().strftime('%Y-%m-%d')}


@app.route('/')
@app.route('/index')
def index():
    """
    Главная страница. Содержит список статей с общей информацией,
    ссылкой на статью на v1.ru и ссылкой на страницу статьи интерфейса
    """
    back = request.referrer or '/'

    page = request.args.get('page', 0, type=int)

    sort = request.args.get('sort', None)
    order = request.args.get('order', 0, type=int)

    if sort in ['title', 'date', 'author', 'sentence']:
        o = '-' if order else ''
    else:
        sort = 'date'
        o = '-'

    if sort == 'sentence':
        sort = 'sentence_count'

    connect(DEFAULT_DATABASE, DEFAULT_DATABASE)
    count = Article.objects.count()

    # Считаем количество страниц
    page_count = math.ceil(count / PER_PAGE)

    # Достаём статьи из БД, отсортировав в порядке убывания даты,
    # а затем выбираем нужные для текущей страницы
    article_list = Article.objects.order_by(o + sort)[page * PER_PAGE: (page+1) * PER_PAGE]

    # Рендерим шаблон с указанием параметров
    result = render_template(
        'index.html',
        count=count,   # Общее число статей
        articles=article_list,  # Список статей

        # Параметры навигации
        navparams={
            'page': page,  # Текущая страница
            'count': page_count,  # Общее число страниц
            'previous': page > 0,  # Есть ли предыдущая
            'next': page < page_count - 1  # Есть ли следующая
        },

        back=back
        )
    disconnect(DEFAULT_DATABASE)
    return result


@app.route('/articles/<article_id>')
def articles(article_id):
    """
    Страница статьи. Показывает название, дату публикации,
    количество просмотров и комментариев и текст статьи

    :param article_id: ID статьи в базе данных
    """
    back = request.referrer or '/'

    connect(DEFAULT_DATABASE, DEFAULT_DATABASE)
    # Извлекаем статью по id
    try:
        article = Article.objects(id=article_id).get()

        # sentences = Sentence.objects(src_to_article=article)
        sentences = []

    except (ValidationError, DoesNotExist):

        article = None
        sentences = []

    # Рендерим шаблон
    result =  render_template(
        'articles.html',
        article=article,
        sentences=sentences,
        back=back)
    disconnect(DEFAULT_DATABASE)
    return result


@app.route('/parse')
def parse():
    n = request.args.get('n', 1, int)
    date = request.args.get('date', '')

    try:
        if date:
            date = datetime.strptime(date, '%Y-%m-%d')
            col = run_pars_date(date)

        else:
            col = run_pars_kol(n)

    except Exception as e:
        print_exc()

        return jsonify({
            'code': 500, 'name': 'Internal server error',
            'message': 'Error while finding synonyms', 'exc': str(e)
        })

    else:
        return jsonify({'code': 200, 'name': 'OK', 'count': col})


@app.errorhandler(404)
def not_found(e):
    return render_template('error.html', error=e)
