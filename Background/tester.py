from konlpy.tag import Kkma
from similar import getSimKey, getSimKeyPath, getSimKeyOld, tokenizedKey
from smtp import sendAll

os_path = 'model/ko.bin'
own_path = 'model/ko_own.bin'
combined_path = 'model/ko_modified.bin'
old_path = 'model/Kkma_dataset.model'
test_path = 'model/ko_test.model'

# Old -> type = 0
# New -> type = 1

def printSim(keyword, type):
    if type == 0:
         print(getSimKeyPath(keyword, 5, own_path))# 크로우
    elif type == 1:
        print("기존 프로젝트 모델 : ", getSimKeyOld(keyword, 5)) # 이전프로젝트
    elif type == 2:
        #print("개선 프로젝트 모델 : ", getSimKey(keyword, 5)) # 스킵
        print("개선 프로젝트 모델 : ", getSimKeyPath(keyword, 5, test_path))
    elif type == 3:
        print("OS 모델 : ", getSimKeyPath(keyword, 5, os_path)) # os
    elif type == 4:
        print("Test 모델 : ", getSimKeyPath(keyword, 5, test_path))  # os

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


    return print(tokenized_data)

# ================================================TEST CALL======================================================#
texts = ["학점", "공모전", "취업", "채용", "등록금", "개학", "전과",
         "예비군", "박람회", "중앙도서관", "반납", "취득", "동아리",
         "복수전공", "휴학", "아코", "축제", "방학", "신청", "계절학기"]

for text in texts:
    print("[", text, "] 에 대한 유사단어 5개 추출")
    for i in range (1,4):
        printSim(text,i)
    print("")

