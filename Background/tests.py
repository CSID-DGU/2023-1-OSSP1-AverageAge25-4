import unittest
from similar import getSimKey, tokenizedKey, cleanText, getDB
import re
from smtp import sendAll


def test():
    print(2/0)


class MyTestCase(unittest.TestCase):
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
