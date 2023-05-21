import environ
from pathlib import Path
import os
import re
import MySQLdb
from konlpy.tag import Kkma
from gensim.models.word2vec import Word2Vec

os_path = '../model/ko.bin'
own_path = '../model/ko_own.bin'
combined_path = '../model/ko_combined.bin'


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

def buildModel():
    data_set = []
    title_list = getDB()
    count = 0
    is_built = False

    for title in title_list:
        preprocessed = tokenized(title)
        data_set.append(preprocessed)
        count += 1

        # 초기 빌드 데이터
        if count >= 50:
            if is_built:
                model = Word2Vec.load(own_path)
                model.build_vocab(data_set, update=True)
                model.train(data_set, total_examples=model.corpus_count, epochs=model.epochs)
                model.save(own_path)

            else:
                model = Word2Vec(data_set, size=200, window=5, min_count=1, workers=4)
                model.save(own_path)
                is_built = True

            count = 0
            data_set = []


    print("성공")

def trainModel(load_path, saved_path):
    data_set = []
    title_list = getDB()
    count = 0

    for title in title_list:
        preprocessed = tokenized(title)
        data_set.append(preprocessed)
        count += 1
        if count >= 50:
            model = Word2Vec.load(load_path)
            model.build_vocab(data_set, update=True)
            model.train(data_set, total_examples=model.corpus_count, epochs=model.epochs)
            model.save(saved_path)
            count = 0
            data_set = []

    print("성공")

def getSimKey(keyword, num):
    try:
        model = Word2Vec.load(combined_path)
        similar_words = model.wv.most_similar(keyword, topn=num)
        similar_words = [word for word, score in similar_words if score >= 0]
        return similar_words

    except KeyError:
        print(f"{keyword} is not in vocabulary")

        return []

# own_path = notice title 학습 모델
# os_path = Kyubyong OS 사전 학습 모델
# combined_path = 합친 모델
def getSimKeyTester(keyword, num, path):
    try:
        model = Word2Vec.load(path)
        similar_words = model.wv.most_similar(keyword, topn=num)
        similar_words = [word for word, score in similar_words if score >= 0]
        return similar_words

    except KeyError:
        print(f"{keyword} is not in vocabulary")

        return []