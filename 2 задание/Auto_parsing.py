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
    db = client.SemaDB
    news = db.news

    i = 0

    # Цикл, который обходит все статьи в коллекции
    for articles in news.find():
        i += 1
        print(i)
        # print(articles)

        file = open('/home/dima/tomita-parser/build/bin/input.txt', 'w')  # открытие в режиме записи
        statya = str(articles.get("content"))
        # очистка от лишних символов
        statya = statya.replace("['", "")
        statya = statya.replace("']", "")
        statya = statya.replace("'", "")
        statya = statya.replace("',", "")
        statya = statya.replace(".,", ".")
        file.write(statya)  # запись статьи в файл
        file.close()  # закрытие файла

        os.chdir('/home/dima/tomita-parser/build/bin')
        # запуск томита-парсера
        os.system('./tomita-parser config.proto')
        os.chdir('/home/dima/Lingvistika_Sema/tomita')

        # получаем предложения
        sentens = ""
        f = open("/home/dima/tomita-parser/build/bin/output.html", "r")
        contents = f.read()
        soup = BeautifulSoup(contents, 'html.parser')
        for tag in soup.find('table').findAll('a'):
            sentens += str("{1}".format(tag.name, tag.text) + " ")

        f.close()

        sentens = sentens.replace("'", "")
        sentens = sentens.replace(" .,", ".")

        ID = articles.get("_id")

        news.find_one_and_update({'_id': ObjectId(ID)}, {"$set": {'sentens': sentens}})
