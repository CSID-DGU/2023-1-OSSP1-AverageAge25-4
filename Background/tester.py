from konlpy.tag import Kkma
from similar import getSimKey, getSimKeyTester, getSimKeyOld, tokenized
from smtp import sendAll

os_path = 'model/ko.bin'
own_path = 'model/ko_own.bin'
combined_path = 'model/ko_combined.bin'
old_path = 'model/Kkma_dataset.model.bin'

# Old -> type = 0
# New -> type = 1

def printSim(keyword, type):
    if type == 0:
        print(getSimKeyOld(keyword, 5))
    elif type == 1:
        print(getSimKeyTester(keyword, 5, own_path))
    elif type == 2:
        print(getSimKey(keyword, 5))

    else:
        print("put 0 or 1 in type")



def sendTest():
    sendAll()

def printTokenizedOld(data):

    new_data = data.replace("[^ㄱ-ㅎㅏ-ㅣ가-힣 ]", "")  # 데이터 정규표현식 -> 특수문자 제거

    stop_words = []
    with open('model/stopword.txt', encoding='utf-8') as f:
        for i in f:
            stop_words.append(i.strip())

    kkma = Kkma()

    tokenized_sentence = kkma.nouns(new_data)
    tokenized_data = [word for word in tokenized_sentence if not word in stop_words]  # 불용어 제거


    return tokenized_data

# ================================================TEST CALL======================================================#

printSim("취업", 0)
printSim("삼성 전자 취업", 1)
printSim("삼성 전자 취업", 2)