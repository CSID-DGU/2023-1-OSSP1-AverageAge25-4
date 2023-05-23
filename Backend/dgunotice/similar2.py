import re
from gensim.models import Word2Vec
from konlpy.tag import Kkma

path = 'Backend/dgunotice/ko_combined.bin'

def cleanText(data):
    first_process = re.sub(r"[^\uAC00-\uD7A30-9a-zA-Z\s]", "", data) # 특수문자 제거
    second_process = re.sub(r"[0-9]", "", first_process) # 숫자 제거
    cleaned_data = second_process.strip() # 좌측 우측 양측 공백 제거
    return cleaned_data


def tokenizedKey(data):
    cleaned_data = cleanText(data)
    kkma = Kkma()
    preprocessed = kkma.nouns(cleaned_data)

    return preprocessed


def getSimKeyBasePath(keyword, num, path):
    try:
        model = Word2Vec.load(path)
        similar_words = model.wv.most_similar(tokenizedKey(keyword), topn=num)
        similar_words = [word for word, score in similar_words if score >= 0]
        return similar_words

    except KeyError:
        print(f"{keyword} is not in vocabulary")

        return []


def getSimKeyPath(keyword, num, path):
    keywords_tokenized = tokenizedKey(keyword)  # 키워드 토큰화

    keywords_similar = []

    for keyword_tokenized in keywords_tokenized:
        keywords_similar += getSimKeyPath(keyword_tokenized, num, path)

        return keywords_similar

