## Установить mongodb

Подробная инструкция по установке приведена на официальном сайте MongoDB: https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-ubuntu/

## Установить библиотеки на питон (через pip3):

    pip3 install -r requirements.txt

## Установка Томита-парсера:

Ссылка на гит с парсером: https://github.com/yandex/tomita-parser/

Выполняем следующие команды в терминале:

- sudo apt-get install build-essential cmake lua5.2
- git clone https://github.com/yandex/tomita-parser
- cd tomita-parser && mkdir build && cd build
- cmake ../src/ -DCMAKE_BUILD_TYPE=Release
- make
- копируем libmystem-c-binding.so из https://github.com/yandex/tomita-parser/releases/tag/v1.0 в ту же папку

## Запускать через консоль (по SSH)

Для прямого парсинга, до 10_000 записей

	python3 main.py

Для запуска сайта

    python3 -m web
