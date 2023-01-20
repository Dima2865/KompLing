import traceback
from bs4 import BeautifulSoup
from mongoengine import connect, disconnect
from sentence_parsing import pars_sentence
from tonality import classify_sentences
from db import DEFAULT_DATABASE, Article
import dateparser
import datetime, json, requests

api_link = 'https://s02.api.yc.kpcdn.net/content/api/1/pages/get.json?pages.age.month={month}&pages.age.year={year}&pages.direction=page&pages.number={day}&pages.target.class=100&pages.target.id=5'
id_news = 5056192
url = 'https://www.volgograd.kp.ru/online/news/{0}/'


def get_links(date):
    year = date.year
    month = date.month
    day = date.day
    link = api_link.format(day=day, month=month, year=year)
    content = requests.get(link).json()
    links = []
    for child in content["childs"]:
        links.append(url.format(child["@id"]))
    return links


def get_article(link):
    soup = BeautifulSoup(requests.get(link).text, 'lxml')
    title = soup.find("h1", ["sc-j7em19-3", "ktyjXw"]).text
    date = soup.find("span", ["sc-j7em19-1", "eDdTDf"]).text
    try:
        author = soup.find("span", ["sc-1jl27nw-1", "bPIqer"]).text
    except AttributeError:
        author = None
    paragraphs = soup.find_all("p", ["sc-1wayp1z-16", "iRDJAt"])
    content = [p.text for p in paragraphs]
    return {
        'url': link,
        'title': title,
        'content': content,
        'author': author,
        'date': dateparser.parse(date),
    }


def get_articles(links):
    articles = []
    for i, link in enumerate(links):
        print(f"parse art {i + 1}: {link}")
        try:
            articles.append(get_article(link))
        except Exception:
            print(f"Error parsing {link}")
            traceback.print_exc()
    return articles


def main(n=10_000):
    date = datetime.date.today()
    connect(DEFAULT_DATABASE, DEFAULT_DATABASE)
    db_col = Article.objects.count()
    while db_col < n:
        col = 0
        articles = get_articles(get_links(date))
        date -= datetime.timedelta(1)
        for article in articles:
            a = Article.objects(url=article["url"]).first()
            if a is None:
                a = Article(**article)
                pars_sentence(a)
                classify_sentences(a)
                a.save()
                col += 1
        db_col += col
        print(f"saved {col} records for {date}. Total {db_col}")
    disconnect(DEFAULT_DATABASE)


def run_pars_kol(n):
    date = datetime.date.today()
    connect(DEFAULT_DATABASE, DEFAULT_DATABASE)
    db_col = Article.objects.count()
    n += db_col
    new_col = 0
    while db_col < n:
        col = 0
        articles = get_articles(get_links(date))
        date -= datetime.timedelta(1)
        for article in articles:
            a = Article.objects(url=article["url"]).first()
            if a is None:
                a = Article(**article)
                pars_sentence(a)
                classify_sentences(a)
                a.save()
                col += 1
        db_col += col
        new_col += col
        print(f"saved {col} records for {date}. Total {db_col}")
    disconnect(DEFAULT_DATABASE)

    return new_col


def run_pars_date(date):
    connect(DEFAULT_DATABASE, DEFAULT_DATABASE)
    db_col = Article.objects.count()
    col = 0
    articles = get_articles(get_links(date))
    for article in articles:
        a = Article.objects(url=article["url"]).first()
        if a is None:
            a = Article(**article)
            pars_sentence(a)
            classify_sentences(a)
            a.save()
            col += 1
    db_col += col
    print(f"saved {col} records for {date}. Total {db_col}")
    disconnect(DEFAULT_DATABASE)

    return col


if __name__ == '__main__':
    main()
