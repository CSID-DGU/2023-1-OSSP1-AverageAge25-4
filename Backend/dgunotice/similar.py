import gensim
import tqdm as tqdm
import pandas as pd
from models import Notice
from konlpy.tag import Kkma
from gensim.models.word2vec import Word2Vec

model_path = '../model/ko.bin'

def getDataSet():
    data_set = Notice.objects.values_list('title', flat=True)
    return data_set

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

def trainModel():
    model = gensim.models.Word2Vec.load(mode_path)
    model.build_vocab(tokenized(), update=True)
    model.train(tokenized(), total_examples=model.corpus_count, epochs=model.epochs)
    model.save(model_path)


# # 정확한 순서대로 5개
# def getSimKey(model_path, keyword):
#     model = Word2Vec.load(model_path)
#     similar_words = model.wv.most_similar(keyword, topn=5)
#     similar_words = [word for word, similarity in similar_words]
#
#     return similar_words


#정확도 조정, -1 < accuracy < 1 범위에서 높을수록 정확

def getSimKey(path, keyword, accuracy, num):
    model = Word2Vec.load(path)
    try:
        similar_words = model.wv.most_similar(keyword, topn=num)
        similar_words = [(word, score) for word, score in similar_words if score >= accuracy]
        return similar_words
    except KeyError:
        print(f"{keyword} is not in vocabulary")

        return []


# print(getSimKey(model0_path, "학사", 0.8,5))
