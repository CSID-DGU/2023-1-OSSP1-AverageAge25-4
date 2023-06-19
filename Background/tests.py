import unittest
from pathlib import Path
import os
import environ

from similar import getSimKey, tokenizedKey, cleanText, getDB, buildModelTest
from smtp import sendAll, sendEmail

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
    env_file=os.path.join(BASE_DIR, 'Backend', '.env')
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

    def test_getDB(self):
        self.maxDiff = None
        result = getDB()
        self.assertGreater(len(result), 0)

        pass

    def test_build_model_initial(self):
        size = 300
        window = 300
        test_path = 'model/test_model.bin'
        result = buildModelTest(size, window, test_path)
        self.assertTrue(result)


class SmtpTestCase(unittest.TestCase):
    def test_sendAll(self):
        result = sendAll()
        self.assertTrue(result)

        pass

    def test_sendEmail(self):
        send_list = []
        send_list.append(env('NAVER_ADDRESS'))
        title = "test_title"
        link = "test_link"
        result = sendEmail(send_list, title, link, 0)
        self.assertTrue(result)

        pass