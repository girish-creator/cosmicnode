import unittest
import requests
import os
import sys
sys.path.append(os.path.abspath(os.curdir))
sys.path.append(os.path.dirname(os.path.abspath(os.curdir)))
from source import mqtt_handler, serial_com_handler, configuration


class AllTests(unittest.TestCase):
    def setUp(self):
        self.mqtt_client = mqtt_handler.MqttHandler()
        self.mqtt_client.make_connection()
        self.ser_obj = serial_com_handler.SerialConn()
        self.ser_obj.connect()

    def tearDown(self):
        self.mqtt_client.disconnect()
        self.ser_obj.disconnect()
        configuration.MQTT_MESSAGE_RX = False

    def test_cosmic_api1(self):
        response = requests.get('https://chercher.tech/sample/api/product/read?id=90')
        #response = requests.get('http://192.168.1.27/rpc/Command.PWM')
        #response = requests.post('http://192.168.1.27/rpc/Command.PWM, headers={Content-Type: text/plain}, data={"cmd":51,"address":32827,"params":[1,1,0]}')
        #self.assertEquals(response.status_code, {'payload': '{"cmd":51,"address":32827,"params":[1,1,0,0,0]}', 'headers': "{'Content-Type': 'text/plain'}"})
        response = requests.post('http://10.58.46.237/rpc/Command.PWM', headers={"Content-Type": "application/json"}, json={"cmd":208,"address": 65535, "params":[0,1,0]})
        message = self.ser_obj.wait_for_message()

        #response = requests.post('http://192.168.68.107/rpc/Command.PWM, headers={Content-Type: text/plain}, data={"cmd":51,"address":32827,"params":[1,1,0,0,0]}')
        #self.assertEquals(response.status_code, {'payload': '{"cmd":51,"address":32827,"params":[1,1,0,0,0]}', 'headers': "{'Content-Type': 'text/plain'}"})

        # mqtt_client_0 = mqtt_handler.MqttHandler()
        # mqtt_client_0.make_connection()
        # self.assertEquals(mqtt_client_0.subscribe_topic('test/girish/msg', 'Hello World!'), 'Hello World!')
        # self.assertEquals(mqtt_client_0.subscribe_topic('test/girish/msg', 'Hello World!'), 'Hello World!')

        mqtt_client_1 = mqtt_handler.MqttHandler()
        mqtt_client_1.make_connection()
        self.assertEquals(mqtt_client_1.publish_topic('test/girish/msg', 'Hello World!'), 'mqtt message content to find in the mqtt logs')
        self.assertEquals(mqtt_client_1.publish_topic('test/girish/msg', 'Hello World!'), 'mqtt messages contents to find in the mqtt client logs')
        response_0 = requests.get('https://chercher.tech/sample/api/product/read?id=90')
        response_1 = requests.post('http://10.58.46.237/rpc/Command.PWM, headers=http://10.58.46.237/rpc/Command.PWM, data={Content-Type: text/plain}')
        self.assertEquals(response_1.status_code, {'payload': '{"cmd":51,"address":32827,"params":[1,1,0,0,0]}', 'headers': "{'Content-Type': 'text/plain'}"})

        message = self.ser_obj.wait_for_message()
        mqtt_client_0 = mqtt_handler.MqttHandler()
        mqtt_client_0.make_connection()
        self.assertEquals(mqtt_client_0.subscribe_topic('test/girish/msg', 'Hello World!'), 'Hello World!')
        self.assertEquals(mqtt_client_0.subscribe_topic('test/girish/msg', 'Hello World!'), 'Hello World!')

        mqtt_client_1 = mqtt_handler.MqttHandler()
        mqtt_client_1.make_connection()
        self.assertEquals(mqtt_client_1.publish_topic('test/girish/msg', 'Hello World!'), 'mqtt message content to find in the mqtt logs')
        self.assertEquals(mqtt_client_1.publish_topic('test/girish/msg', 'Hello World!'), 'mqtt messages contents to find in the mqtt client logs')


    def test_cossmisc_api1(self):
        response_0 = requests.get('https://chercher.tech/sample/api/product/read?id=90')
        response_1 = requests.post('http://10.58.46.237/rpc/Command.PWM, headers=http://10.58.46.237/rpc/Command.PWM, data={Content-Type: text/plain}')
        self.assertEquals(response_1.status_code, {'payload': '{"cmd":51,"address":32827,"params":[1,1,0,0,0]}', 'headers': "{'Content-Type': 'text/plain'}"})

        message = self.ser_obj.wait_for_message()
        mqtt_client_0 = mqtt_handler.MqttHandler()
        mqtt_client_0.make_connection()
        self.assertEquals(mqtt_client_0.subscribe_topic('test/girish/msg', 'Hello World!'), 'Hello World!')
        self.assertEquals(mqtt_client_0.subscribe_topic('test/girish/msg', 'Hello World!'), 'Hello World!')

        mqtt_client_1 = mqtt_handler.MqttHandler()
        mqtt_client_1.make_connection()
        self.assertEquals(mqtt_client_1.publish_topic('test/girish/msg', 'Hello World!'), 'mqtt message content to find in the mqtt logs')
        self.assertEquals(mqtt_client_1.publish_topic('test/girish/msg', 'Hello World!'), 'mqtt messages contents to find in the mqtt client logs')


    def test_cossmsisc_api1(self):
        response_0 = requests.get('https://chercher.tech/sample/api/product/read?id=90')
        response_1 = requests.post('http://10.58.46.237/rpc/Command.PWM', headers={'Content-Type': 'application/json'}, json={"cmd":210,"address":65535,"params":[50]})
        self.assertEquals(response_1.status_code, 200)

        message = self.ser_obj.wait_for_message()
        self.assertEqual(message, 'LGT_CMD_LIGHT_BRIGHTNESS: 5')

        mqtt_client_0 = mqtt_handler.MqttHandler()
        mqtt_client_0.make_connection()
        mqtt_client_0.subscribe_topic('test/girish/msg', 'Hello World!')
        self.assertEquals(configuration.MQTT_MESSAGE_RX, True)
        self.assertEquals(configuration.MQTT_MESSAGE_RX, True)

        mqtt_client_1 = mqtt_handler.MqttHandler()
        mqtt_client_1.make_connection()
        mqtt_client_1.publish_topic('test/girish/msg', 'Hello World!')
        self.assertEquals(configuration.MQTT_MESSAGE_RX, 'mqtt message content to find in the mqtt logs')
        self.assertEquals(configuration.MQTT_MESSAGE_RX, 'mqtt messages contents to find in the mqtt client logs')


    def test_all_cossmsisc_api1(self):
        response_0 = requests.post('http://10.58.46.237/rpc/Command.PWM', headers={'Content-Type': 'application/json'}, json={"cmd":210,"address":65535,"params":[50]})
        self.assertEquals(response_0.status_code, 200)

        message = self.ser_obj.wait_for_message()
        self.assertEquals(message, 'LGT_CMD_LIGHT_BRIGHTNESS: 50')

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
