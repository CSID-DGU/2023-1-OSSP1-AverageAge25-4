import re
from cryptography.fernet import Fernet
import base64


#공백 제외 숫자/문자만 남도록
#정규 표현식 사용
def str_replace(input_str, form='[^\w]'):
    #정규 표현식 입력
    pattern = re.compile(form)
    return pattern.sub('', input_str)

#암호화 (ASCII)
#대칭키 방식 Crytography.Fernet 모듈 사용 (AES 방식)
#키 값 변경 설계 예정
#키 관리 방식 정의 필요
class Key:
    def __init__(self):
        self.key = b''
        self.load_key()

    #키 생성 (서버에 키 저장)
    def generate_key(self):
        new_key = Fernet.generate_key()
        self.key = new_key

        #키 생성 경로(저장 위치 정해야함)
        path1 = 'mykey.key'
        with open(path1, 'wb') as mykey:
            mykey.write(new_key)

    #저장된 키 로드
    def load_key(self):
        path1 = 'mykey.key'
        try:
            with open(path1, 'rb') as mykey:
                self.key = mykey.read()
        except FileNotFoundError:
            print('key 파일이 존재하지 않습니다')

    def encrypt(self, input):
        f = Fernet(self.key)
        encpt_input = f.encrypt(input.encode('ascii'))
        return encpt_input.decode('ascii')

    def decrypt(self, input):
        f = Fernet(self.key)
        decpt_input = f.decrypt(input.encode('ascii'))
        return decpt_input.decode('ascii')


#사용법

# keytest.generate_key() 키 생성 (서버 생성 시 최초 1회만 수동으로 실행/키 값 변경시 수행(추천 :6개월~1년))
# 이미 키 값 생성해 놓아서 할 필요 없습니다.

# keytest = Key() 객체 생성
# keytest.encrypt(input) 암호화
# keytest.decrypt(input) 복호화


