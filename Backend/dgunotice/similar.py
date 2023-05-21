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

def getDataSetInitial():
    try:
        connection = MySQLdb.connect(
            host=env('DATABASE_HOST'),
            user=env('DATABASE_USER'),
            passwd=env('DATABASE_PASSWORD'),
            db=env('DATABASE_NAME')
        )
        cursor = connection.cursor()

        cursor.execute("SELECT title FROM Notice")

        rows = cursor.fetchall()

        data_set = [row[0] for row in rows]

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


def tokenizedInitial():
    db_data = getDataSetInitial()
    db_data = pd.DataFrame(db_data, columns=['제목'])
    db_data['제목'] = db_data['제목'].str.replace("[^ㄱ-ㅎㅏ-ㅣ가-힣 ]", "")

    stop_words = []
    with open('stopword.txt', encoding='utf-8') as f:
        for i in f:
            stop_words.append(i.strip())

    kkma = Kkma()

    tokenized_data = []

    for sentence in tqdm.tqdm(db_data['제목']):
        tokenized_sentence = kkma.nouns(sentence)
        stopwords_removed_sentence = [word for word in tokenized_sentence if not word in stop_words]
        tokenized_data.append(stopwords_removed_sentence)

    return tokenized_data

# 전처리
def tokenized():
    db_data = getDataSet()
    db_data = pd.DataFrame(db_data, columns=['제목'])
    db_data['제목'] = db_data['제목'].str.replace("[^ㄱ-ㅎㅏ-ㅣ가-힣 ]", "")

    stop_words = []
    with open('stopword.txt', encoding='utf-8') as f:
        for i in f:
            stop_words.append(i.strip())

    kkma = Kkma()

    tokenized_data = []

    for sentence in tqdm.tqdm(db_data['제목']):
        tokenized_sentence = kkma.nouns(sentence)
        stopwords_removed_sentence = [word for word in tokenized_sentence if not word in stop_words]
        tokenized_data.append(stopwords_removed_sentence)

    return tokenized_data

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
        similar_words = [(word, score) for word, score in similar_words if score >= accuracy]
        return similar_words
    except KeyError:
        print(f"{keyword} is not in vocabulary")

        return []


# print(getSimKey("학사", 0.8,5))
