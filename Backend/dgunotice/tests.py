import unittest
from pathlib import Path
import MySQLdb
from SecurityModule import Key
from similar2 import getSimKey, tokenizedKey, cleanText
from verification import generate_token, verify_email_token, generate_verification_link
import os
import environ
from django.contrib.auth.hashers import make_password
from cryptography.fernet import Fernet

env = environ.Env(
    DATABASE_NAME=(str, ''),
    DATABASE_USER=(str, ''),
    DATABASE_PASSWORD=(str, ''),
    DATABASE_HOST=(str, ''),
    DATABASE_PORT=(str, ''),
    NAVER_ADDRESS=(str, ''),
    NAVER_ID=(str, ''),
    NAVER_PASSWORD=(str, ''),
)

BASE_DIR = Path(__file__).resolve().parent.parent

environ.Env.read_env(
    env_file=os.path.join(BASE_DIR, '.env')
)

class SimilarTestCase(unittest.TestCase):

    def test_similar(self):
        test_word = "공모전"
        test_number = 5
        similar_words = getSimKey(test_word, test_number)

        # 5개의 유사단어가 추출되는지
        self.assertEqual(len(similar_words), test_number)

        # 추출되는 단어가 str 타입인지
        for similar_word in similar_words:
            self.assertTrue(isinstance(similar_word, str))
        pass

    def test_tokenized_key(self):
        test_key = "띄어쓰기 제거 하는지 테스트"
        result = tokenizedKey(test_key)
        self.assertNotIn(" ", result)

        pass

    def test_clean_text(self):
        test_input = "@12특수문자"
        result = cleanText(test_input)
        self.assertRegex(result, '^[가-힣]+$')

        pass

class VerificationTestCase(unittest.TestCase):
    def test_generate_token(self):
        result = generate_token()
        self.assertEqual(len(result), 20)

        pass

    def test_verify_email_token(self):

        key = Key()

        connection = MySQLdb.connect(
            host=env('DATABASE_HOST'),
            user=env('DATABASE_USER'),
            passwd=env('DATABASE_PASSWORD'),
            db=env('DATABASE_NAME')
        )

        cursor = connection.cursor()
        uid = "test@ntest.com"
        crypted_uid = key.encrypt("test@ntest.com")
        password = "1234"
        tok = 'test_token'

        query = """
            INSERT INTO verify (temp_id, temp_password, token)
            VALUES (%s, %s, %s)
        """

        cursor.execute(query, (crypted_uid, password, tok))
        connection.commit()
        connection.close()

        result = verify_email_token(uid, tok, key)
        self.assertEqual(True, result)

        pass
    def test_generate_verification_link(self):
        uid = "test@test.com"
        tok = 'test@test.com'
        result = generate_verification_link(uid, tok)
        self.assertEqual(result, "http://127.0.0.1:8000/verify/?email=test@test.com&token=test@test.com")

