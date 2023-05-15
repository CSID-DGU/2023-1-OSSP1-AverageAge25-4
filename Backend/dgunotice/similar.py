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
