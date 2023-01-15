from bs4 import BeautifulSoup
import requests
import lxml
import os
import time

from bson import ObjectId
from pymongo import MongoClient

if __name__ == '__main__':
    # Подключение к MongoDB, выбор нужной БД и коллекции
    client = MongoClient()
    db = client.Final_ling_db
    news = db.news

    i = 0

    sentence = []

    # Цикл, который обходит все статьи в коллекции
    for articles in news.find():
        i += 1
        print(i)
        # print(articles)

        sentence.append(str(articles.get("sentens")))

    with open(r'/home/dima/sentences.txt', 'w') as file:  # открытие в режиме записи
        for sent in sentence:
            if len(sent) != 0:
                file.write(sent + '\n')
