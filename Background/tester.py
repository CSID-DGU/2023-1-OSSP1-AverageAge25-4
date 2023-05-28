import string
from random import random

from django.contrib.auth.tokens import default_token_generator
from konlpy.tag import Kkma
from similar import getSimKey, getSimKeyPath, getSimKeyOld, buildModelInitial
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

def printTest():
    paths = ['model/window1.bin', 'model/window2.bin', 'model/window3.bin', 'model/window4.bin', 'model/window5.bin',
             'model/window6.bin', 'model/window7.bin', 'model/window8.bin', 'model/window9.bin', 'model/window10.bin', 'model/window11.bin', 'model/window12.bin', 'model/window13.bin', 'model/window14.bin', 'model/window15.bin', 'model/window16.bin', 'model/window17.bin', 'model/window18.bin', 'model/window19.bin', 'model/window20.bin']

    texts = ["학점", "공모전", "취업", "채용", "등록금", "개학", "전과",
             "예비군", "박람회", "중앙도서관", "반납", "취득", "동아리",
             "복수전공", "휴학", "아코", "축제", "방학", "신청", "계절학기"]

    for text in texts:
        i = 1
        for path in paths:
            print("window = [", i, "], keyword = [", text, "]")
            print(getSimKeyPath(text, 5, path))
            i += 1
        print("")


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

import secrets

def generate_token(length=15):
    token = secrets.token_urlsafe(length)
    return token
# ================================================TEST CALL======================================================#


print(generate_token())