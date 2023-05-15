import tqdm as tqdm
import pandas as pd
from models import Notice
from konlpy.tag import Kkma
from gensim.models.word2vec import Word2Vec

model0_path = 'model/Kkma_dataset.model'
# 아래 모델들은 테스트 예정
model1_path = 'model/Hannanum_dataset.model'
model2_path = 'model/Komoran_dataset.model'
model3_path = 'model/Okt_dataset.model'
model4_path = 'model/Mecab_dataset.model'

def getDataSet():
    data_set = Notice.objects.values_list('title', flat=True)
    return data_set

# 전처리
def tokenize():
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



