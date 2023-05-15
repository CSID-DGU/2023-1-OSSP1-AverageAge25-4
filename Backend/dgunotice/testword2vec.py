import tqdm as tqdm
import pandas as pd
from models import Notice
from konlpy.tag import Kkma
from gensim.models.word2vec import Word2Vec

def getDB():
    db_data = Notice.objects.values_list('title', flat=True)
    return db_data

def tokenizeData():
    db_data = getDB()
    db_data = pd.DataFrame(db_data, columns = ['제목'])
    db_data['제목'] = db_data['제목'].str.replace("[^ㄱ-ㅎㅏ-ㅣ가-힣 ]","")

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

def setModel():
    tokenized_data = tokenizeData()
    global model
    model = Word2Vec(sentences = tokenized_data, sg=1)
    model.save('model/new_Kkma_dataset.model')
    return model

def findVocab(set):
    model=Word2Vec.load(set)
    word_vectors=model.wv
    vocabs=word_vectors.vocab.keys()
    remove_key=[]
    print("제거전")
    print(vocabs)
    for i in vocabs:
        if len(i)==1:
            remove_key.append(i)
    for key in list(vocabs) :
        if key in remove_key :
            del word_vectors.vocab[key]
    print("제거후")
    vocabs=word_vectors.vocab.keys()
    print(vocabs)
    return vocabs