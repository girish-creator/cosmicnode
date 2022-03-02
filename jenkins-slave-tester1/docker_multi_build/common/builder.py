import os
import configuration
import json
import logging


class TestBuilderException(Exception):
    pass


class TestBuilder:
    def __init__(self, test_name, api_endpoint, mqtt_message_check=False, serial_message_check=False, argument_dict=dict):
        self.root_logger = logging.getLogger(name="builder.log")
        self.test_name = test_name
        if str(test_name).__contains__('android'):
            self.module_name = "test_android_api.py"
            self.template_name = "android_api_tests.json"
        else:
            self.module_name = "test_api.py"
            self.template_name = "api_tests.json"
        self.api_endpoint = api_endpoint
        self.mqtt_message_check = mqtt_message_check
        self.serial_message_check = serial_message_check
        self.argument_dict = argument_dict
        self.test_folder_path = os.path.join(configuration.ROOT_PATH, "tests")
        self.test_template_path = os.path.join(self.test_folder_path, "templates_for_tests")
        self.complete_text = ""

    def run(self):
        self.root_logger.info("starting test builder")
        self.get_module_name()
        self.define_testcase()
        self.write_data_to_test_file()

    def get_module_name(self):
        try:
            if (self.api_endpoint is None) or (self.api_endpoint == ""):
                raise TestBuilderException("Cannot create a test without an API endpoint")
            if (self.mqtt_message_check is True) and (self.serial_message_check is True):
                self.module_name = "test_all.py"
                self.template_name = "all_tests.json"
            if self.mqtt_message_check is True:
                self.module_name = "test_mqtt.py"
                self.template_name = "mqtt_tests.json"
            if self.serial_message_check is True:
                self.module_name = "test_serial.py"
                self.template_name = "serial_tests.json"
        except Exception as error:
            raise TestBuilderException(str.format("builder: get_module_name: {0}", error))

    def create_argument_list(self):
        for key, value in self.argument_dict.items():
            yield value

    def define_testcase(self):
        try:
            argument_list = list()
            # get the test template json file
            # format the argument dictionary
            # update the template in json
            # generate the testcase in text
            with open(os.path.join(self.test_template_path, self.template_name), 'r') as file_obj:
                test_template_json = json.load(file_obj)

            for key, value in test_template_json.items():
                if key.lower() == 'test_name':
                    test_template_json['test_name'] = self.test_name
                if key.lower() == 'api_to_test':
                    test_template_json['api_to_test'] = self.api_endpoint
                    try:
                        argument_list = next(self.create_argument_list())
                    except StopIteration:
                        break
                    test_template_json['verifications'] = self.generate_verification_list(argument_list,
                                                                                          test_template_json)
                if key.lower() == 'test_type':
                    test_template_json['test_type'] = self.generate_verification_list_all_tests(test_template_json)

            self.generate_api_test_from_json(test_template_json)
        except Exception as error:
            raise TestBuilderException(str.format("builder: define_testcase: {0}", error))

    def generate_verification_list_all_tests(self, test_template_json):
        try:
            test_verifications = list()
            x = self.api_endpoint
            return test_verifications
        except Exception as error:
            raise TestBuilderException(str.format("builder: define_testcase: {0}", error))

    def generate_verification_list(self, argument_list, test_template_json):
        try:
            verifications = list()
            for argument_dict in argument_list:
                for arg_key, arg_value in argument_dict.items():
                    for item in test_template_json['verifications']:
                        for item_key, item_value in item.items():
                            if item_key == arg_key:
                                argument_dict[item_key] = arg_value
                verifications.append(argument_dict)
            return verifications
        except Exception as error:
            raise TestBuilderException(str.format("builder: generate_verification_list: {0}", error))

    def generate_api_test_from_json(self, json_template):
        try:
            function_name = str.format("def {0}(self)", json_template['test_name'])
            requests_get_statement = str.format("response = requests.get('{0}')", json_template['api_to_test'])
            assert_statements = list()
            for verification_dict in json_template['verifications']:
                assert_statements.append(str.format("self.{0}(response.{1}, {2})", verification_dict['assertion_type'],
                                                    verification_dict['assertion_parameter'],
                                                    verification_dict['expected_value']))
            part_one_test = str.format("\n    {0}:\n"
                                       "        {1}\n", function_name, requests_get_statement)
            ver_steps = ""
            for item in assert_statements:
                ver_steps = ver_steps + str.format("        {0}\n", item)

            self.complete_text = part_one_test + ver_steps
        except Exception as error:
            raise TestBuilderException(str.format("builder: generate_api_test_from_json: {0}", error))

    def write_data_to_test_file(self):
        try:
            with open(os.path.join(self.test_folder_path, self.module_name), 'r') as file_obj:
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
    args = {'api_args': [{"assertion_type": "assertEquals", "assertion_parameter": "status_code",
                          "expected_value": 200},
                         {"assertion_type": "assertEquals", "assertion_parameter": "status_code",
                          "expected_value": 200}
                         ]}
    test_builder_obj = TestBuilder(test_name= 'test_new_fgsgadtpp',
                                   api_endpoint="https://chercher.tech/sample/api/product/read?id=90",
                                   argument_dict=args)
    test_builder_obj.run()
