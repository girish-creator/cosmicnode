import unittest
import requests
import os


class MqttTests(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_new_mqtt(self):
        response = requests.get('https://chercher.tech/sample/api/product/read?id=90')
        self.assertEquals(response.status_code, 200)
