import environ
from pathlib import Path
import os
import re
import MySQLdb
import gensim
from konlpy.tag import Kkma
from gensim.models.word2vec import Word2Vec
from gensim.models import Word2Vec

os_path = 'model/ko.bin'
own_path = 'model/ko_own.bin'
modified_path = 'model/ko_modified.bin'
old_path = 'model/Kkma_dataset.model'
test_path = 'model/ko_test.model'

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

def getDB():
    try:
        connection = MySQLdb.connect(
            host=env('DATABASE_HOST'),
            user=env('DATABASE_USER'),
            passwd=env('DATABASE_PASSWORD'),
            db=env('DATABASE_NAME')
        )

        cursor = connection.cursor()

        cursor.execute("SELECT title FROM Notice WHERE isTrained = FALSE")

        rows = cursor.fetchall()

        data_set = [row[0] for row in rows]

        update_query = "UPDATE Notice SET isTrained = TRUE WHERE isTrained = FALSE"
        cursor.execute(update_query)

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
    with open('model/stopword.txt', encoding='utf-8') as f:
        for i in f:
            stop_words.append(i.strip())

    kkma = Kkma()

    tokenized_sentence = kkma.nouns(cleaned_data)
    preprocessed = [word for word in tokenized_sentence if not word in stop_words]  # 불용어 제거

    return preprocessed

# 불용어가 키워드일 경우 토큰화 진행시 Empty list가 생길수있어서
# 따로 불용어를 제거한 tokenizedKey 정의
def tokenizedKey(data):

    preprocessed = data.split(" ")

    return preprocessed

def buildModel():
    data_set = []
    title_list = getDB()
    count = 0
    cnt = 0
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
                cnt += 50
                print(cnt, "개 완료")

            else:
                model = Word2Vec(data_set, size=200, window=5, min_count=1, workers=4)
                model.save(own_path)
                is_built = True

            count = 0
            data_set = []


    print("성공")

def buildModelInitial(size, window, path):
    data_set = []
    title_list = getDB()

    for title in title_list:
        preprocessed = tokenized(title)
        data_set.append(preprocessed)

    model = Word2Vec(data_set, size=size, window=window, min_count=1, workers=4, sg = 1)
    model.save(path)



    print("성공")

def trainModelSelf(load_path, saved_path):
    data_set = []
    title_list = getDB()
    count = 0
    cnt = 0
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
            cnt += 50
            print(cnt, "개 완료")

    print("성공")

def trainModel():
    data_set = []
    title_list = getDB()
    count = 0

    for title in title_list:
        preprocessed = tokenized(title)
        data_set.append(preprocessed)
        count += 1
        if count >= 50:
            model = Word2Vec.load(modified_path)
            model.build_vocab(data_set, update=True)
            model.train(data_set, total_examples=model.corpus_count, epochs=model.epochs)
            model.save(modified_path)
            count = 0
            data_set = []

    print("성공")


# 키워드에 대한 유사단어 num개 추출
def getSimKeyBase(keyword, num):
    try:
        model = Word2Vec.load(modified_path)
        similar_words = model.wv.most_similar(keyword, topn=num)
        similar_words = [word for word, score in similar_words if score >= 0]
        return similar_words

    except KeyError:
        print(f"{keyword} is not in vocabulary")

        return []

# own_path = notice title 학습 모델
# os_path = Kyubyong OS 사전 학습 모델
# combined_path = 합친 모델
def getSimKeyBasePath(keyword, num, path):
    try:
        model = Word2Vec.load(path)
        similar_words = model.wv.most_similar(tokenizedKey(keyword), topn=num)
        similar_words = [word for word, score in similar_words if score >= 0]
        return similar_words

    except KeyError:
        print(f"{keyword} is not in vocabulary")

        return []

# 키워드를 토큰화하여 토큰 마다 유사단어 num개 추출
def getSimKey(keyword, num):
    keywords_tokenized = tokenizedKey(keyword)  # 키워드 토큰화

    keywords_similar = []

    for keyword_tokenized in keywords_tokenized:
        keywords_similar += getSimKeyBase(keyword_tokenized, num)

    return keywords_similar


def getSimKeyPath(keyword, num, path):
    keywords_tokenized = tokenizedKey(keyword)  # 키워드 토큰화

    keywords_similar = []

    for keyword_tokenized in keywords_tokenized:
        keywords_similar += getSimKeyBasePath(keyword_tokenized, num, path)

    return keywords_similar

def getSimKeyOld(keyword, num):
    try:
        model = gensim.models.word2vec.Word2Vec.load(old_path)
        similar_words = model.wv.most_similar(keyword, topn=num)
        similar_words = [word for word, score in similar_words if score >= 0]
        return similar_words

    except KeyError:
        print(f"{keyword} is not in vocabulary")

        return []

