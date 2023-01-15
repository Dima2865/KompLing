from pyspark.sql import SparkSession
from pyspark.ml.feature import Word2VecModel
from pprint import pprint
import os
import sys
import numpy as np
from pyspark.ml.feature import Tokenizer
from pyspark.ml.feature import StopWordsRemover
from pyspark.ml.feature import Word2Vec
import re
import string
import datetime
sys.path.append("..")

PATH = 'context_synonyms/'
PATH2 = 'data_text/*.txt'


def find_synonyms(elements, model, spark_session, count=5):
    result = []
    for element in elements:
        try:
            elementDF = spark_session.createDataFrame(
                [(element[0].lower().split(" "),)],
                ["words"])
            transform_elem = model.transform(elementDF)
            synonyms = model.findSynonyms(transform_elem.collect()[0][1], count).collect()
            result.append(synonyms)
        except Exception:
            result.append([])

    return result


def remove_punctuation(text):
    # Удаление пунктуации из текста
    return text.translate(str.maketrans('', '', string.punctuation))


def get_only_words(tokens):
    # Получение списка токенов, содержащих только слова
    return list(filter(lambda x: re.match('[а-яА-Я]+', x), tokens))


def create_w2v_model():
    spark = SparkSession \
        .builder \
        .appName("SimpleApplication") \
        .config("spark.executor.memory", "2g") \
        .config("spark.driver.memory", "2g") \
        .config("spark.memory.offHeap.enabled", True) \
        .config("spark.memory.offHeap.size", "2g") \
        .getOrCreate()

    input_file = spark.sparkContext.wholeTextFiles(PATH2)

    print("Подготовка данных.")
    prepared_data = input_file.map(lambda x: (x[0], remove_punctuation(x[1])))

    print("Подготовка данных..")
    df = prepared_data.toDF()

    print("Подготовка данных...")
    prepared_df = df.selectExpr('_2 as text')

    print("Разбитие на токены")
    tokenizer = Tokenizer(inputCol='text', outputCol='words')
    words = tokenizer.transform(prepared_df)

    print("Очистка от стоп-слов")
    stop_words = StopWordsRemover.loadDefaultStopWords('russian')
    remover = StopWordsRemover(inputCol="words", outputCol="filtered", stopWords=stop_words)

    print("Построение модели")
    word2Vec = Word2Vec(vectorSize=50, inputCol='words', outputCol='result', minCount=2)
    model = word2Vec.fit(words)

    print("Сохранение модели")
    today = datetime.datetime.today()
    model_name = today.strftime("context_synonyms/")

    print("Model " + model_name + " saved")
    model.save(model_name)

    spark.stop()


if __name__ == '__main__':
    print("Выберите нужный пункт: ")
    print("1) Создать новую модель")
    print("2) Использовать ранее созданную")

    number = int(input("Введите номер пункта: "))

    if number == 1:
        create_w2v_model()
    elif number == 2:
        print("Используется ранее созданная модель.")
    else:
        print("Введен неверный номер!")
        sys.exit(0)

    slovo = str(input("Введите нужное слово или словосочетание: "))

    with SparkSession.builder.appName("SimpleApplication").getOrCreate() as spark_session:
        model = Word2VecModel.load(PATH)

        print("Поиск контекстных синонимов: ")
        persons_synonyms = find_synonyms(slovo, model, spark_session)
        pprint(persons_synonyms)
