import unittest
import requests
import os
from common import mqtt_handler, serial_com_handler, configuration


class SerialTests(unittest.TestCase):
    def setUp(self):
        self.ser_obj = serial_com_handler.SerialConn()
        self.ser_obj.connect()

    def tearDown(self):
        self.ser_obj.disconnect()
        configuration.MQTT_MESSAGE_RX = False

    def test_new_serial(self):
        response = requests.get('https://chercher.tech/sample/api/product/read?id=90')
        self.assertEquals(response.status_code, 200)

    def test_cossmsisc_api1(self):
        response_1 = requests.post('http://192.168.1.27/rpc/Command.PWM', headers={'Content-Type': 'application/json'},
                                   json={"cmd":210,"address":65535,"params":[50]})
        self.assertEquals(response_1.status_code, 200)

        message = self.ser_obj.wait_for_message()
        self.assertEquals(message, 'LGT_CMD_LIGHT_BRIGHTNESS: 5')

