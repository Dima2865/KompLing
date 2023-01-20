"""Анализ тональностей предложений"""

from pymystem3 import Mystem
from nltk.corpus import stopwords
from nltk import NaiveBayesClassifier

import re, string, random
import csv

import os
import pickle

from tqdm import tqdm

CLASSIFIER_PATH = 'data/model.pickle'
TWEETS_PATH = 'data/Tweets'

my_stem = Mystem()
ru_stopwords = stopwords.words('russian')


def prepare_tweet(tweet):
    # Убрать ссылки и обращения
    tweet = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*(),]|'
                   '(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', tweet)

    tweet = re.sub("(@[A-Za-z0-9_]+)", "", tweet)

    tweet = re.sub(r"([:;=_-]*[)(]+)|"
                   r"([:;=_-]+[D*]+)|"
                   r"([D]+[:;=_-]+)|"
                   r"([)(]+[:;=_-]*)|"
                   r"(\*_\*)|(\^_\^)", "", tweet)

    # Токенизировать и лемматизировать
    tokens = [token.strip() for token in my_stem.lemmatize(tweet.lower())]

    cleaned_tokens = []

    # Отфильтровать пунктуацию и стоп слова
    for token in tokens:
        if len(token) > 0 and token not in string.punctuation and token not in ru_stopwords:
            cleaned_tokens.append(token)

    return cleaned_tokens


def load_tweets():
    with open(os.path.join(TWEETS_PATH, 'positive.csv'), 'r', encoding='utf-8') as positive:
        positive_tweets = [row[3] for row in csv.reader(positive, delimiter=';')]

    with open(os.path.join(TWEETS_PATH, 'negative.csv'), 'r', encoding='utf-8') as negative:
        negative_tweets = [row[3] for row in csv.reader(negative, delimiter=';')]

    return positive_tweets, negative_tweets


def load_documents():
    with open(os.path.join(TWEETS_PATH, 'documents.csv'), encoding='utf-8-sig') as file:
        return [*csv.reader(file, delimiter=';')]


re_link = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*(),]|'
                     r'(?:%[0-9a-fA-F][0-9a-fA-F]))+')

re_at = re.compile(r'(@[A-Za-z0-9_]+)')

re_smile = re.compile(r'([:;=_-]*[)(]+)|'
                      r'([:;=_-]+[D*]+)|'
                      r'([D]+[:;=_-]+)|'
                      r'([)(]+[:;=_-]*)|'
                      r'(\*_\*)|(\^_\^)')


def prepare_sentence(sentence):
    sentence = re.sub(re_link, '', sentence)
    sentence = re.sub(re_at, '', sentence)
    sentence = re.sub(re_smile, '', sentence)
    # Токенизировать и лемматизировать
    tokens = [token.strip() for token in my_stem.lemmatize(sentence.lower())]
    cleaned_tokens = []
    # Отфильтровать пунктуацию и стоп слова
    for token in tokens:
        if len(token) > 0 and token not in string.punctuation and token not in ru_stopwords:
            cleaned_tokens.append(token)

    return {token: True for token in cleaned_tokens}


def train_model():
    print('--- Training tonality classifier ---')
    print('Loading dataset')
    documents = load_documents()
    # Подготовить твиты для обучения модели
    dataset = [(prepare_sentence(document), str(score))
               for document, score in tqdm(documents, desc='Tokenizing')]
    print('Shuffling')
    random.shuffle(dataset)
    print('Training')
    bayes = NaiveBayesClassifier.train(dataset)
    print('Saving')
    # Сохраняем классификатор
    os.makedirs(os.path.dirname(CLASSIFIER_PATH), exist_ok=True)
    with open(CLASSIFIER_PATH, 'wb') as file:
        pickle.dump(bayes, file)
    print('--- Classifier trained ---')


def load_model():
    with open(CLASSIFIER_PATH, 'rb') as file:
        return pickle.load(file)


def classify(sentence):
    return classifier.classify({token: True for token in prepare_sentence(sentence)})


def classify_sentences(article):
    tonalities = []
    for sentence in article.sentence:
        tonalities.append(float(classify(sentence)))
    article.tonality = tonalities


# Тренирует модель и сохраняет в файл, если файл не найден
if not os.path.exists(CLASSIFIER_PATH):
    train_model()

classifier = load_model()
