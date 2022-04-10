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

    def test_new_fgsgadtpp(self):
        response = requests.get('https://chercher.tech/sample/api/product/read?id=90')
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.status_code, 200)

    def test_new_gadtpp(self):
        response = requests.get('https://chercher.tech/sample/api/product/read?id=90')
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.status_code, 200)

    def test_new_gassdtpp(self):
        response = requests.get('https://chercher.tech/sample/api/product/read?id=90')
        self.assertEquals(response.status_code, 200)
        self.assertEqual(response.status_code, 300)

    def test_cosmic_api1(self):
        payload = "{\"cmd\":51,\"address\":32827,\"params\":[1,1,0,0,0]}"
        headers = {
            'Content-Type': 'text/plain'
        }
        response = requests.request("POST", 'http://192.168.1.27/rpc/Command.PWM', headers=headers, data=payload)
        self.assertEquals(response.status_code, 200)


    def test_api_cossmsisc_api1(self):
        response_0 = requests.post('http://192.168.1.27/rpc/Command.PWM', headers={'Content-Type': 'application/json'}, json={"cmd":210,"address":65535,"params":[50]})
        self.assertEquals(response_0.status_code, 200)

