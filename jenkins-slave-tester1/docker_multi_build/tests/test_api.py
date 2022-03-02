import unittest
import requests
import os


class ApiTests(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_new(self):
        response = requests.get('https://chercher.tech/sample/api/product/read?id=90')
        self.assertEquals(response.status_code, 200)
