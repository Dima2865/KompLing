Конф. файлы для парсера - в этой папке находятся конфигурационные файлы для работы Томита-парсера

Поиск контекстных синонимов - в данной папке находится программа для поиска контекстных синонимов

Auto_parsing.py - программа, которая берет по одной статье из MongoDB, далее запускается Томита-парсер, потом полученные предложения заносятся обратно в БД.

get_strings_for_syn.py - программа для выгрузки предложений с упоминаниями из БД в тектовый файл для дальнейшего использования программой для поиска контекстных синонимов.

news_final - экспорт базы данных в формате .json

--------------------------------------------------

Руководство по установке и пользованию.

Необходимо установить Oracle VM VirtualBox. Скачать можно с официального сайта Oracle: https://www.oracle.com/virtualization/technologies/vm/downloads/virtualbox-downloads.html 
Далее устанавливаем ОС Ubuntu 18.04 на виртуальную машину. Скачать с официального сайта Ubuntu: https://releases.ubuntu.com/18.04/
Дальнейшие действия производятся в ОС Ubuntu 18.04.

Установка Томита-парсера: 

Ссылка на гит с парсером: https://github.com/yandex/tomita-parser/

Выполняем следующие команды в терминале:

•	sudo apt-get install build-essential cmake lua5.2

•	git clone https://github.com/yandex/tomita-parser

•	cd tomita-parser && mkdir build && cd build

•	cmake ../src/ -DCMAKE_BUILD_TYPE=Release

•	make

•	копируем libmystem-c-binding.so из https://github.com/yandex/tomita-parser/releases/tag/v1.0 в ту же папку

Установка базы данных MongoDB:

Подробная инструкция по установке приведена на официальном сайте MongoDB: https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-ubuntu/
Так же потребуется установить MongoDB Compass для более удобной и понятной работы с данной базой данных.
Ссылка на инструкцию по установке:   
https://www.mongodb.com/docs/compass/master/install/ 

Для запуска программ по поиску именованных сущностей и контекстных синонимов, написанных на языке Python нужно будет установить IDE PyCharm Community, либо использовать терминал Ubuntu с предустановленным в системе языком Python.
