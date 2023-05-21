import environ
from pathlib import Path
import os
import MySQLdb
import gensim
import tqdm as tqdm
import pandas as pd
from konlpy.tag import Kkma
from gensim.models.word2vec import Word2Vec


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
    env_file=os.path.join(BASE_DIR, 'Backend', '.env')
)
print(env('DATABASE_NAME'))
def getDataSetInitial():
    try:
        connection = MySQLdb.connect(
            host=env('DATABASE_HOST'),
            user=env('DATABASE_USER'),
            passwd=env('DATABASE_PASSWORD'),
            db=env('DATABASE_NAME')
        )
        cursor = connection.cursor()
        print(env('DATABASE_PASSWORD'))
        cursor.execute("SELECT title FROM Notice")

        rows = cursor.fetchall()

        data_set = [row[0] for row in rows]



        print(data_set)

        cursor.close()
        connection.close()
        return data_set

    except Exception as e:
        # 예외 처리
        print('An error occurred:', str(e))

def getDataSet():
    try:
        connection = MySQLdb.connect(
            host=env('DATABASE_HOST'),
            user=env('DATABASE_USER'),
            passwd=env('DATABASE_PASSWORD'),
            db=env('DATABASE_NAME')
        )
        cursor = connection.cursor()

        cursor.execute("SELECT title FROM Notice AND isSended = False")

        rows = cursor.fetchall()

        data_set = [row[0] for row in rows]

        cursor.close()
        connection.close()

        return data_set

    except Exception as e:
        # 예외 처리
        print('An error occurred:', str(e))


def tokenized(data):

    stop_words = []
    with open('stopword.txt', encoding='utf-8') as f:
        for i in f:
            stop_words.append(i.strip())

    kkma = Kkma()

    tokenized_sentence = kkma.nouns(data)
    preprocessed_data = [word for word in tokenized_sentence if not word in stop_words]  # 불용어 제거


    return preprocessed_data


def trainModelInitial():
    model = gensim.models.Word2Vec.load(model_path)
    model.build_vocab(tokenizedInitial(), update=True)
    model.train(tokenizedInitial(), total_examples=model.corpus_count, epochs=model.epochs)
    model.save(model_path)

def trainModel():
    model = gensim.models.Word2Vec.load(model_path)

    model.build_vocab(tokenized(), update=True)
    print("test")
    model.train(tokenized(), total_examples=model.corpus_count, epochs=model.epochs)
    model.save(model_path)


def getSimKey(keyword, accuracy, num):
    model = Word2Vec.load(model_path)
    try:
        similar_words = model.wv.most_similar(keyword, topn=num)
        similar_words = [ word for word, score in similar_words if score >= accuracy]
        return similar_words
    except KeyError:
        print(f"{keyword} is not in vocabulary")

        return []



print(getDataSetInitial())