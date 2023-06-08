from django.test import TestCase
from similar import getDB, buildModelInitial, getSimKey

class SimilarTestCase(TestCase):
    def test_getSimKey(self):
        getDB();
        pass