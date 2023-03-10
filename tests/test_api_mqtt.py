import unittest
import requests
import sys
import os
sys.path.append(os.path.abspath(os.curdir))
sys.path.append(os.path.dirname(os.path.abspath(os.curdir)))
from source import mqtt_handler, configuration


class MqttTests(unittest.TestCase):
    def setUp(self):
        self.mqtt_client = mqtt_handler.MqttHandler()
        self.mqtt_client.make_connection()
        pass

    def tearDown(self):
        self.mqtt_client.disconnect()
        pass

    def test_new_mqtt(self):
        response = requests.get('https://chercher.tech/sample/api/product/read?id=90')
        self.assertEquals(response.status_code, 200)

    def test_cosmic_api1(self):
        response = requests.get('https://chercher.tech/sample/api/product/read?id=90')
        response = requests.post('http://192.168.1.27/rpc/Command.PWM, headers={Content-Type: text/plain}, data={"cmd":51,"address":32827,"params":[1,1,0,0,0]}')
        self.assertEquals(response.status_code, {'payload': '{"cmd":51,"address":32827,"params":[1,1,0,0,0]}', 'headers': "{'Content-Type': 'text/plain'}"})

        mqtt_client_0 = mqtt_handler.MqttHandler()
        mqtt_client_0.make_connection()
        self.assertEquals(mqtt_client_0.subscribe_topic('test/girish/msg', 'Hello World!'), 'Hello World!')
        self.assertEquals(mqtt_client_0.subscribe_topic('test/girish/msg', 'Hello World!'), 'Hello World!')

        mqtt_client_1 = mqtt_handler.MqttHandler()
        mqtt_client_1.make_connection()
        self.assertEquals(mqtt_client_1.publish_topic('test/girish/msg', 'Hello World!'), 0)
        self.assertEquals(mqtt_client_1.publish_topic('test/girish/msg', 'Hello World!'), 'mqtt messages contents to find in the mqtt client logs')


    def test_mqtt_cossmsisc_api1(self):
        response_0 = requests.post('http://192.168.1.27/rpc/Command.PWM', headers={'Content-Type': 'application/json'}, json={"cmd":210,"address":65535,"params":[50]})
        self.assertEquals(response_0.status_code, 200)

        mqtt_client_0 = mqtt_handler.MqttHandler()
        mqtt_client_0.make_connection()
        mqtt_client_0.subscribe_topic('test/girish/msg', 'Hello World!')
        self.assertEquals(configuration.MQTT_MESSAGE_RX, 'Hello World!')
        self.assertEquals(configuration.MQTT_MESSAGE_RX, 'Hello World!')

        mqtt_client_1 = mqtt_handler.MqttHandler()
        mqtt_client_1.make_connection()
        mqtt_client_1.publish_topic('test/girish/msg', 'Hello World!')
        self.assertEquals(configuration.MQTT_MESSAGE_RX, 'mqtt message content to find in the mqtt logs')
        self.assertEquals(configuration.MQTT_MESSAGE_RX, 'mqtt messages contents to find in the mqtt client logs')


if __name__ == '__main__':
    unittest.main()