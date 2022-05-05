from common import configuration
import ssl
import paho.mqtt.client as paho
import logging
import os
import time


class MqttHandler:
    def __init__(self):
        self.client = paho.Client()
        self.mqtt_server = configuration.MQTT_SERVER
        self.mqtt_port = configuration.MQTT_PORT
        self.mqtt_keep_alive = configuration.MQTT_KEEP_ALIVE
        self.mqtt_topic = "test/girish/msg"
        self.logger = logging.getLogger(name="mqtt_handler.log")
        self.message = ""
        self.counter = 0

    def make_connection(self):
        self.logger.info("connecting to broker")
        self.client.username_pw_set(username="5qSJjR8c8GBHpQTM", password="plaVW4Q9NXTvY8lu")
        print(os.path.join(configuration.CA_CERTIFICATE_PATH, "ca.crt"))
        self.client.tls_set(os.path.join(configuration.CA_CERTIFICATE_PATH, "ca.crt"), tls_version=ssl.PROTOCOL_TLSv1_2)
        self.client.connect(self.mqtt_server, self.mqtt_port, self.mqtt_keep_alive)
        self.logger.info(str.format("Successfully connected to broker {0}", self.mqtt_server))

    def on_message(self, client, userdata, message):
        self.counter += 1
        self.logger.info(message.payload.decode("utf-8"))
        if self.message in message.payload.decode("utf-8"):
            self.client.loop_stop()
            self.client.disconnect()
            configuration.MQTT_MESSAGE_RX = True
            print(str.format("Message {0} found in mqtt message {1}", self.message, message.payload.decode("utf-8")))

    def on_log(self, client, userdata, level, buffer):
        self.logger.info(str.format("Log: {0}", buffer))

    def subscribe(self, message, qos=1, options=None, properties=None):
        self.logger.info(str.format("Subscribing to event: {0}", self.mqtt_topic))
        self.client.subscribe(self.mqtt_topic, 1)
        self.logger.info("Topic Subscribed")

    def publish(self, payload=None, qos=1, retain=False, properties=None):
        self.logger.info(str.format("Subscribing to event: {0}", self.mqtt_topic))
        pub_response = self.client.publish(self.mqtt_topic, payload, 1)
        self.logger.info("Published to Topic")
        return pub_response

    def subscribe_topic(self, topic, message):
        self.mqtt_topic = topic
        self.logger.info("overriding existing mqtt methods")
        self.client.on_message = self.on_message
        self.client.on_log = self.on_log
        self.client.on_connect = self.subscribe
        self.logger.info(str.format("Listening to event: {0}", self.mqtt_topic))
        self.message = message
        self.client.loop_forever()

    def publish_topic(self, topic, message):
        self.mqtt_topic = topic
        self.logger.info("overriding existing mqtt methods")
        self.client.on_message = self.on_message
        self.client.on_log = self.on_log
        response = self.publish(message)
        self.logger.info(str.format("Published message to topic: {0}", self.mqtt_topic))
        return response

    def disconnect(self):
        self.client.disconnect()


if __name__ == "__main__":
    client_obj = MqttHandler()
    client_obj.make_connection()
    x = client_obj.subscribe_topic(topic="test/girish/msg", message="Hi Girish")
    responses = client_obj.publish_topic(topic="test/girish/msg",
                                         message="Hi Girish, thi is published again",)
    print(responses)