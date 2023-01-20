from bs4 import BeautifulSoup
import os


def pars_sentence(article):

    user_dir = os.path.expanduser('~/')
    tomita_path = os.path.join(user_dir, 'tomita-parser/build/bin')

    start_dir = os.getcwd()

    with open(os.path.join(tomita_path, 'input.txt'), 'w') as file:  # открытие в режиме записи
        file.write(article.text)  # запись статьи в файл

    os.chdir(tomita_path)
    # запуск томита-парсера
    os.system('./tomita-parser config.proto')
    os.chdir(start_dir)

    # получаем предложения
    sentences = []
    with open(os.path.join(user_dir, "tomita-parser/build/bin/output.html"), "r") as f:
        contents = f.read()
        soup = BeautifulSoup(contents, 'html.parser')
        for tag in soup.find('table').findAll('a'):
            sentences.append(tag.text.replace("'", "").replace(" .,", "."))

    article.sentence = sentences
