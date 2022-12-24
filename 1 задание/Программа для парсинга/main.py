import traceback
from bs4 import BeautifulSoup
# from selenium import webdriver
# from selenium.webdriver.common.by import By
from mongoengine import connect, disconnect

import db
from db import DEFAULT_DATABASE, Article
import dateparser
from selenium.common.exceptions import NoSuchElementException
import datetime, json, requests
api_link = 'https://s02.api.yc.kpcdn.net/content/api/1/pages/get.json?pages.age.month={month}&pages.age.year={year}&pages.direction=page&pages.number={day}&pages.target.class=100&pages.target.id=5'
# url = 'https://www.volgograd.kp.ru/online/'
id_news = 5056192
url = 'https://www.volgograd.kp.ru/online/news/{0}/'
# options = webdriver.FirefoxOptions()
# options.add_argument('--headless')


def getLinks(date):
    year = date.year
    month = date.month
    day = date.day
    link = api_link.format(day=day, month=month, year=year)
    content = requests.get(link).json()
    links = []
    for child in content["childs"]:
        links.append(url.format(child["@id"]))
    return links


def getArticle(link):
    # driver = webdriver.Firefox(options=options)
    # driver.get(link)
    soup = BeautifulSoup(requests.get(link).text, 'lxml')
    # title = driver.find_element(By.CSS_SELECTOR, "h1.sc-j7em19-3.ktyjXw").text
    title = soup.find("h1", ["sc-j7em19-3", "ktyjXw"]).text
    #date = driver.find_element(By.CSS_SELECTOR, "span.sc-j7em19-1.eDdTDf").text
    date = soup.find("span", ["sc-j7em19-1", "eDdTDf"]).text
    try:
        # author = driver.find_element(By.CSS_SELECTOR, "span.sc-1jl27nw-1.bPIqer").text
        author = soup.find("span", ["sc-1jl27nw-1", "bPIqer"]).text
    except AttributeError:
        author = None

    #paragraphs = driver.find_elements(By.CSS_SELECTOR, "p.sc-1wayp1z-16.iRDJAt")
    paragraphs = soup.find_all("p", ["sc-1wayp1z-16", "iRDJAt"])

    content = [p.text for p in paragraphs]

    # driver.close()

    return {
        'url': link,
        'title': title,
        'content': content,
        'author': author,
        'date': dateparser.parse(date),
    }


def getArticles(links):
    articles = []
    for i, link in enumerate(links):
        print(f"parse art {i + 1}: {link}")
        try:
            articles.append(getArticle(link))
        except Exception:
            print(f"Error parsing {link}")
            traceback.print_exc()

    return articles


def main():
    date = datetime.date.today()
    # date = datetime.date(2021, 7, 25)
    connect(DEFAULT_DATABASE, DEFAULT_DATABASE)
    db_col = Article.objects.count()
    while db_col < 10_000:
        col = 0
        articles = getArticles(getLinks(date))
        date -= datetime.timedelta(1)
        for article in articles:
            a = Article.objects(url=article["url"]).first()
            if a is None:
                Article(**article).save()
                col += 1
        db_col+=col
        print(f"saved {col} records for {date}. Total {db_col}")
    disconnect(DEFAULT_DATABASE)


if __name__ == '__main__':
    main()