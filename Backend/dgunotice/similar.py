import environ
from pathlib import Path
import os
import re
import MySQLdb
import gensim
import tqdm as tqdm
import pandas as pd
from konlpy.tag import Kkma
from gensim.models.word2vec import Word2Vec
from gensim.models import KeyedVectors


model_path = '../model/ko.bin'

env = environ.Env(
    DATABASE_NAME=(str, ''),
    DATABASE_USER=(str, ''),
    DATABASE_PASSWORD=(str, ''),
    DATABASE_HOST=(str, ''),
    DATABASE_PORT=(str, ''),
)

BASE_DIR = Path(__file__).resolve().parent.parent

environ.Env.read_env(
    env_file=os.path.join(BASE_DIR, '.env')
)


def getDB():
    try:
        connection = MySQLdb.connect(
            host=env('DATABASE_HOST'),
            user=env('DATABASE_USER'),
            passwd=env('DATABASE_PASSWORD'),
            db=env('DATABASE_NAME')
        )

        cursor = connection.cursor()

        cursor.execute("SELECT title FROM Notice WHERE isSended = TRUE")

        rows = cursor.fetchall()

        data_set = [row[0] for row in rows]

        cursor.close()
        connection.close()

        return data_set

    except Exception as e:
        # 예외 처리
        print('An error occurred:', str(e))


# 정규표현식
def cleanText(data):
    first_process = re.sub(r"[^\uAC00-\uD7A30-9a-zA-Z\s]", "", data) # 특수문자 제거
    second_process = re.sub(r"[0-9]", "", first_process) # 숫자 제거
    cleaned_data = second_process.strip() # 좌측 우측 양측 공백 제거
    return cleaned_data

# 전처리
def tokenized(data):
    cleaned_data = cleanText(data)

    stop_words = []
    with open('stopword.txt', encoding='utf-8') as f:
        for i in f:
            stop_words.append(i.strip())

    kkma = Kkma()

    tokenized_sentence = kkma.nouns(cleaned_data)
    preprocessed = [word for word in tokenized_sentence if not word in stop_words]  # 불용어 제거

    return preprocessed

def trainModelInitial():
    model = gensim.models.Word2Vec.load(model_path)
    model.build_vocab(tokenizedInitial(), update=True)
    model.train(tokenizedInitial(), total_examples=model.corpus_count, epochs=model.epochs)
    model.save(model_path)

def trainModel():
    model = gensim.models.Word2Vec.load(model_path)
    model.build_vocab(tokenized(), update=True)
    model.train(tokenized(), total_examples=model.corpus_count, epochs=model.epochs)
    model.save(model_path)


def getSimKey(keyword, accuracy, num):
    model = Word2Vec.load(model_path)
    try:
        similar_words = model.wv.most_similar(keyword, topn=num)
        similar_words = [word for word, score in similar_words if score >= accuracy]
        return similar_words
    except KeyError:
        print(f"{keyword} is not in vocabulary")

        return []

print(tokenized("안녕하세요 왜 오셨어요"))