import os
MQTT_SERVER = "mqtt3.cosmicnode.com"
MQTT_PORT = 8883
MQTT_KEEP_ALIVE = 60
SERIAL_RX_COM_PORT = "ttyUSB0"
SERIAL_TX_COM_PORT = "ttyUSB1"
SERIAL_NODE_COM_PORT = "ttyUSB2"
VOLUME = ""
ROOT_PATH = os.getcwd()
#ROOT_PATH = "C:\\Users\\Girish-Nair\\Documents\\GitHub\\cosmicnode\\jenkins-slave-tester1\\docker_multi_build"
CA_CERTIFICATE_PATH = os.path.join('home', 'cosmic-node')
SERIAL_RX_BAUD_RATE = 1000000
MQTT_MESSAGE_RX = False