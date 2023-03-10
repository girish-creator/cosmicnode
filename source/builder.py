import os
import configuration
import json
import logging


class TestBuilderException(Exception):
    pass


class TestBuilder:
    def __init__(self, test_name, argument_dict=dict):
        self.logger = logging.getLogger(name="builder.log")
        self.test_name = test_name
        self.argument_dict = argument_dict
        self.test_folder_path = os.path.join(configuration.ROOT_PATH, "tests")
        self.test_template_path = os.path.join(self.test_folder_path, "templates_for_tests")
        self.complete_text = ""
        self.module_name = ""
        self.template_name = ""

    def run(self):
        try:
            self.logger.info("starting test builder")
            self.get_module_name()
            verified_argument_dict = self.generate_test_argument_dict()
            self.define_testcase(verified_argument_dict)
            self.write_data_to_test_file()
        except Exception as error:
            raise TestBuilderException(str.format("builder: run: {0}", error))

    def get_module_name(self):
        try:
            if ('serial' in self.argument_dict) and ('mqtt' in self.argument_dict):
                self.module_name = "test_all.py"
                self.template_name = "all_tests.json"
                self.verify_test_arguments(api_list=True, mqtt_message_check=True,
                                           serial_message_check=True)
                self.test_name = 'test_all_' + self.test_name
            elif 'mqtt' in self.argument_dict:
                self.module_name = "test_api_mqtt.py"
                self.template_name = "api_mqtt_tests.json"
                self.verify_test_arguments(api_list=True, mqtt_message_check=True)
                self.test_name = 'test_mqtt_' + self.test_name
            elif 'serial' in self.argument_dict:
                self.module_name = "test_serial.py"
                self.template_name = "serial_tests.json"
                self.verify_test_arguments(api_list=True, serial_message_check=True)
                self.test_name = 'test_serial_' + self.test_name
            elif str(self.test_name).__contains__('android'):
                if 'android' in self.argument_dict:
                    self.module_name = "test_android_api.py"
                    self.template_name = "android_api_tests.json"
                    self.verify_test_arguments(android_api_list=True)
                    self.test_name = 'test_android_' + self.test_name
                else:
                    raise TestBuilderException("Insufficient argument for creating android test")
            else:
                self.module_name = "test_api.py"
                self.template_name = "api_tests.json"
                self.verify_test_arguments(api_list=True)
                self.test_name = 'test_api_' + self.test_name
        except Exception as error:
            raise TestBuilderException(str.format("builder: get_module_name: {0}", error))

    def verify_test_arguments(self, api_list=False, mqtt_message_check=False, serial_message_check=False,
                              android_api_list=False):
        try:
            key_list = []
            if api_list:
                key_list.append('api_list')
            if mqtt_message_check:
                key_list.append('mqtt')
            if serial_message_check:
                key_list.append('serial')
            if android_api_list:
                key_list.append('android_api_list')

            if len(key_list) == len(self.argument_dict.keys()):
                for key, value in self.argument_dict.items():
                    if key.lower() not in key_list:
                        KeyError(str.format("Key {0} not found in mandatory list {1}", key, key_list))
            else:
                raise IndexError("Insufficient number of arguments")
        except Exception as error:
            raise TestBuilderException(str.format("builder: verify_test_arguments: {0}", error))

    def generate_test_argument_dict(self):
        try:
            argument_list = list()
            # get the test template json file
            # format the argument dictionary
            # update the template in json
            # generate the testcase in text
            with open(os.path.join(self.test_template_path, self.template_name), 'r') as file_obj:
                test_template_json = json.load(file_obj)

            sample_dict = dict()
            for key, value in test_template_json.items():
                if key.lower() == 'test_name':
                    test_template_json['test_name'] = self.test_name
                    sample_dict['test_name'] = self.test_name
                elif key.lower() == 'api_list':
                    ssss = list()
                    for api_item in self.argument_dict['api_list']:
                        for item in test_template_json['api_list']:
                            api_item_operation = api_item['operation'].upper()
                            json_api_operation = item['operation'].upper()
                            if api_item_operation.upper() == json_api_operation.upper():
                                print(str.format("found related item {0}", api_item))
                                if "api_verifications" in api_item.keys():
                                    api_item['api_verifications'] = self.generate_verification_list(
                                        api_item['api_verifications'], item['api_verifications'])
                                ssss.append(api_item)
                                break
                    sample_dict['api_list'] = ssss
                elif key.lower() == 'mqtt':
                    ssss = list()
                    for mqtt_item in self.argument_dict['mqtt']:
                        for item in test_template_json['mqtt']:
                            mqtt_item_operation = mqtt_item['operation'].upper()
                            json_api_operation = item['operation'].upper()
                            if mqtt_item_operation.upper() == json_api_operation.upper():
                                print(str.format("found related item {0}", mqtt_item))
                                if "mqtt_verifications" in mqtt_item.keys():
                                    mqtt_item['mqtt_verifications'] = self.generate_verification_list(
                                        mqtt_item['mqtt_verifications'], item['mqtt_verifications'])
                                ssss.append(mqtt_item)
                                break
                    sample_dict['mqtt'] = ssss
                elif key.lower() == 'serial':
                    ssss = list()
                    for serial_item in self.argument_dict['serial']:
                        for item in test_template_json['serial']:
                            serial_item_operation = serial_item['operation'].upper()
                            json_api_operation = item['operation'].upper()
                            if serial_item_operation.upper() == json_api_operation.upper():
                                print(str.format("found related item {0}", serial_item))
                                if "serial_verifications" in serial_item.keys():
                                    serial_item['serial_verifications'] = self.generate_verification_list(
                                        serial_item['serial_verifications'], item['serial_verifications'])
                                ssss.append(serial_item)
                                break
                    sample_dict['serial'] = ssss
            final_dict = dict()
            for key, value in sample_dict.items():
                if key.lower() == 'test_name':
                    final_dict['test_name'] = sample_dict['test_name']
                if key.lower() == 'api_list':
                    final_dict['api_list'] = sample_dict['api_list']
                elif key.lower() == 'serial':
                    final_dict['serial'] = sample_dict['serial']
            if 'mqtt' in sample_dict:
                final_dict['mqtt'] = sample_dict['mqtt']
            return final_dict
        except Exception as error:
            raise TestBuilderException(str.format("builder: generate_test_argument_dict: {0}", error))

    def define_testcase(self, test_argument_dict):
        try:
            complete_text = ""
            for key, value in test_argument_dict.items():
                if key.lower() == 'test_name':
                    complete_text = str.format("\n    def {0}(self):\n", value)
                elif key.lower() == 'api_list':
                    api_checklist = list()
                    for num, item in enumerate(value):
                        if item['operation'].upper() == "GET":
                            requests_get_statement = str.format("response_{0} = requests.get('{1}')", num,
                                                                item['api_endpoint'])
                            complete_text = complete_text + str.format("        {0}\n", requests_get_statement)
                            if 'api_verifications' in item:
                                complete_text = complete_text + str.format("{0}\n", self.add_verification_steps(
                                    item['api_verifications'], num))
                        elif item['operation'].upper() == "POST":
                            requests_post_statement = str.format("response_{0} = requests.post('{1}', "
                                                                 "headers={2}, json={3})",  num,
                                                                 item['api_endpoint'], item['headers'],
                                                                 item['payload'])
                            complete_text = complete_text + str.format("        {0}\n", requests_post_statement)
                            if 'api_verifications' in item:
                                complete_text = complete_text + str.format("{0}\n", self.add_verification_steps(
                                    item['api_verifications'], num))
                        elif item['operation'].upper() == "PUT":
                            requests_put_statement = str.format("response_{0} = requests.put('{1}, "
                                                                "headers={2}, json={3}, auth={4}')", num,
                                                                item['api_endpoint'], item['headers'],
                                                                item['payload'], item['auth'])
                            complete_text = complete_text + str.format("        {0}\n", requests_put_statement)
                            if 'api_verifications' in item:
                                complete_text = complete_text + str.format("{0}\n", self.add_verification_steps(
                                    item['api_verifications'], num))
                        elif item['operation'].upper() == "DELETE":
                            requests_delete_statement = str.format("response_{0} = requests.delete('{1})", num,
                                                                   item['api_endpoint'],)
                            complete_text = complete_text + str.format("        {0}\n", requests_delete_statement)
                            if 'api_verifications' in item:
                                complete_text = complete_text + str.format("{0}\n", self.add_verification_steps(
                                    item['api_verifications'], num))
                elif key.lower() == 'serial':
                    connect_serial_client = str.format("message = self.ser_obj.wait_for_message()")
                    complete_text = complete_text + str.format("        {0}\n", connect_serial_client)
                    for serial_item in value:
                        if serial_item['operation'].lower() == "read":
                            if 'serial_verifications' in serial_item:
                                complete_text = complete_text + str.format("{0}\n",
                                                                           self.add_serial_verification_steps(
                                                                               serial_item['serial_verifications']))
                elif key.lower() == 'mqtt':
                    for num, mqtt_item in enumerate(value):
                        connect_mqtt_client = str.format("mqtt_client_{0} = mqtt_handler.MqttHandler()", num)
                        complete_text = complete_text + str.format("        {0}\n", connect_mqtt_client)
                        connect_mqtt_client = str.format("mqtt_client_{0}.make_connection()", num)
                        complete_text = complete_text + str.format("        {0}\n", connect_mqtt_client)
                        if mqtt_item['operation'].lower() == "subscribe":
                            connect_mqtt_client = str.format("mqtt_client_{0}.subscribe_topic('{1}', '{2}')",
                                                             num, mqtt_item['topic'],
                                                             mqtt_item['message'])
                            complete_text = complete_text + str.format("        {0}\n", connect_mqtt_client)
                            if 'mqtt_verifications' in mqtt_item:
                                complete_text = complete_text + str.format("{0}\n",
                                                                           self.add_mqtt_verification_steps(
                                                                               mqtt_item['mqtt_verifications']))
                        elif mqtt_item['operation'].lower() == "publish":
                            connect_mqtt_client = str.format("mqtt_client_{0}.publish_topic('{1}', '{2}')",
                                                             num, mqtt_item['topic'],
                                                             mqtt_item['message'])
                            complete_text = complete_text + str.format("        {0}\n", connect_mqtt_client)
                            if 'mqtt_verifications' in mqtt_item:
                                complete_text = complete_text + str.format("{0}\n",
                                                                           self.add_mqtt_verification_steps(
                                                                               mqtt_item['mqtt_verifications']))
            self.complete_text = complete_text
        except Exception as error:
            raise TestBuilderException(str.format("builder: define_testcase: {0}", error))

    def generate_verification_list(self, argument_list, test_template_json):
        try:
            verifications = list()
            for argument_dict in argument_list:
                for arg_key, arg_value in argument_dict.items():
                    for item in test_template_json:
                        for item_key, item_value in item.items():
                            if item_key == arg_key:
                                argument_dict[item_key] = arg_value
                verifications.append(argument_dict)
            return verifications
        except Exception as error:
            raise TestBuilderException(str.format("builder: generate_verification_list: {0}", error))

    def add_verification_steps(self, element, num=None):
        try:
            assert_statements = list()
            for verification_dict in element:
                if num is not None:
                    assert_statements.append(str.format("self.{0}(response_{1}.{2}, {3})",
                                                        verification_dict['assertion_type'], num,
                                                        verification_dict['assertion_parameter'],
                                                        verification_dict['expected_value']))
                else:
                    assert_statements.append(str.format("self.{0}(response.{1}, {2})",
                                                        verification_dict['assertion_type'],
                                                        verification_dict['assertion_parameter'],
                                                        verification_dict['expected_value']))
            ver_steps = ""
            for item in assert_statements:
                ver_steps = ver_steps + str.format("        {0}\n", item)
            return ver_steps
        except Exception as error:
            raise TestBuilderException(str.format("builder: generate_get_api_test_from_json: {0}", error))

    def add_serial_verification_steps(self, element):
        try:
            assert_statements = list()
            for verification_dict in element:
                assert_statements.append(str.format("self.{0}({1}, {2})", verification_dict['assertion_type'],
                                                    verification_dict['assertion_parameter'],
                                                    verification_dict['expected_value']))
            ver_steps = ""
            for item in assert_statements:
                ver_steps = ver_steps + str.format("        {0}\n", item)
            return ver_steps
        except Exception as error:
            raise TestBuilderException(str.format("builder: generate_get_api_test_from_json: {0}", error))

    def add_mqtt_verification_steps(self, element):
        try:
            assert_statements = list()
            for verification_dict in element:
                assert_statements.append(str.format("self.{0}({1}, '{2}')", verification_dict['assertion_type'],
                                                    'configuration.MQTT_MESSAGE_RX',
                                                    verification_dict['expected_value']))
            ver_steps = ""
            for item in assert_statements:
                ver_steps = ver_steps + str.format("        {0}\n", item)
            return ver_steps
        except Exception as error:
            raise TestBuilderException(str.format("builder: generate_get_api_test_from_json: {0}", error))

    def write_data_to_test_file(self):
        try:
            test_file_path = os.path.join(self.test_folder_path, self.module_name)
            with open(test_file_path, 'r') as file_obj:
                file_text = file_obj.read()
                if self.test_name in file_text:
                    raise RuntimeError(str.format("Please choose a different name."
                                                  " Name of this test '{0}' already exists in {1} file.", self.test_name,
                                                  os.path.join(self.test_folder_path, self.module_name)))
                else:
                    with open(os.path.join(self.test_folder_path, self.module_name), 'a') as file_obj:
                        file_obj.write(self.complete_text)
        except Exception as error:
            raise TestBuilderException(str.format("builder: write_data_to_test_file: {0}", error))


if __name__ == "__main__":
    args_api = {'api_list': [{"api_endpoint": "http://192.168.1.27/rpc/Command.PWM",
                          "operation": "POST",
                          "payload": "{\"cmd\":210,\"address\":65535,\"params\":[50]}",
                          "headers": "{'Content-Type': 'application/json'}",
                          'api_verifications': [{"assertion_type": "assertEquals", "assertion_parameter": "status_code",
                                                 "expected_value": 200}
                                                ]
                          },
                             {"api_endpoint": "http://192.168.1.27/rpc/Command.PWM",
                              "operation": "POST",
                              "payload": "{\"cmd\":210,\"address\":65535,\"params\":[50]}",
                              "headers": "{'Content-Type': 'application/json'}",
                              'api_verifications': [
                                  {"assertion_type": "assertEquals", "assertion_parameter": "status_code",
                                   "expected_value": 200}
                                  ]
                              }
                             ]
            }
    args_api_mqtt = {'api_list': [{"api_endpoint": "http://192.168.1.27/rpc/Command.PWM",
                          "operation": "POST",
                          "payload": "{\"cmd\":210,\"address\":65535,\"params\":[50]}",
                          "headers": "{'Content-Type': 'application/json'}",
                          'api_verifications': [{"assertion_type": "assertEquals", "assertion_parameter": "status_code",
                                                 "expected_value": 200}
                                                ]
                          }],
                     'mqtt': [{'operation': 'subscribe',
                          'topic': 'test/girish/msg',
                          'message': 'Hello World!',
                          'mqtt_verifications': [{"assertion_type": "assertEquals", "assertion_parameter": "message",
                                                  "expected_value": "Hello World!"},
                                                 {"assertion_type": "assertEquals", "assertion_parameter": "message",
                                                  "expected_value": "Hello World!"}]},
                         {'operation': 'publish',
                          'topic': 'test/girish/msg',
                          'message': 'Hello World!',
                          'mqtt_verifications': [{"assertion_type": "assertEquals", "assertion_parameter": "message",
                                                  "expected_value": "mqtt message content to find in the mqtt logs"},
                                                 {"assertion_type": "assertEquals", "assertion_parameter": "message",
                                                  "expected_value": "mqtt messages contents to find in the mqtt "
                                                                    "client logs"}]}
                         ],
                    }
    args_api_serial = {'api_list': [{"api_endpoint": "http://192.168.1.27/rpc/Command.PWM",
                          "operation": "POST",
                          "payload": "{\"cmd\":210,\"address\":65535,\"params\":[50]}",
                          "headers": "{'Content-Type': 'application/json'}",
                          'api_verifications': [{"assertion_type": "assertEquals", "assertion_parameter": "status_code",
                                                 "expected_value": 200}
                                                ]
                          }],
                       'serial': [{'operation': 'READ',
                            'serial_verifications': [{"assertion_type": "assertEquals", "assertion_parameter": "message",
                                                      "expected_value": "'LGT_CMD_LIGHT_BRIGHTNESS: 5'"}]}
                         ]
                }
    args_all = {'api_list': [{"api_endpoint": "http://192.168.1.27/rpc/Command.PWM",
                          "operation": "POST",
                          "payload": "{\"cmd\":210,\"address\":65535,\"params\":[50]}",
                          "headers": "{'Content-Type': 'application/json'}",
                          'api_verifications': [{"assertion_type": "assertEquals", "assertion_parameter": "status_code",
                                                 "expected_value": 200}
                                                ]
                          }],
                       'serial': [{'operation': 'READ',
                            'serial_verifications': [{"assertion_type": "assertEquals", "assertion_parameter": "message",
                                                      "expected_value": "'LGT_CMD_LIGHT_BRIGHTNESS: 50'"}]}
                         ],
                     'mqtt': [{'operation': 'subscribe',
                          'topic': 'test/girish/msg',
                          'message': 'Hello World!',
                          'mqtt_verifications': [{"assertion_type": "assertEquals", "assertion_parameter": "message",
                                                  "expected_value": "Hello World!"},
                                                 {"assertion_type": "assertEquals", "assertion_parameter": "message",
                                                  "expected_value": "Hello World!"}]},
                         {'operation': 'publish',
                          'topic': 'test/girish/msg',
                          'message': 'Hello World!',
                          'mqtt_verifications': [{"assertion_type": "assertEquals", "assertion_parameter": "message",
                                                  "expected_value": "mqtt message content to find in the mqtt logs"},
                                                 {"assertion_type": "assertEquals", "assertion_parameter": "message",
                                                  "expected_value": "mqtt messages contents to find in the mqtt "
                                                                    "client logs"}]}
                         ],
                }
    test_builder_obj = TestBuilder(test_name='test_modbus_unique', argument_dict=args_api)
    test_builder_obj.run()
