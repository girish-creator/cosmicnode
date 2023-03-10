import sys
import unittest
import requests
import json
import os
sys.path.append(os.path.abspath(os.curdir))
sys.path.append(os.path.dirname(os.path.abspath(os.curdir)))
from source.utils import get_access_token


class DeviceProfileTests(unittest.TestCase):

    def test_11_create_deviceprofile(self):
        try:
            url = "http://52.59.232.190/api/v1/device-profile?tenantId=62e9669d5ded5e474e2f0281"
            json_path = os.path.join(os.path.dirname(__file__), 'test_data','input', 'create_deviceprofile.json')
            with open(json_path) as json_file:
                payload = json.dumps(json.load(json_file))
                print(payload)
            response = requests.request("POST", url, headers=get_access_token(), data=payload)

            self.assertEqual(response.status_code, 200)
            print(response.json()['data'])
            response_dict = response.json()["data"]
            self.__class__.deviceprofileId = response_dict["_id"]
            print(self.__class__.deviceprofileId)
            keys_to_remove = ["status", "_id", "createdAt", "__v", "children"]
            for key in keys_to_remove:
                response_dict.pop(key)
            validation_payload = json.loads(payload)
            self.assertEqual(response_dict, validation_payload)
            print("device profile\" {} \" successfully created ".format(response_dict['name']))
            print("Test Passed!!!")

        except Exception as error:
            raise error

    def test_12_get_deviceprofile(self):
        try:
            subtenantId = "62e96b215ded5e474e2f035f"
            print(subtenantId)
            print(self.__class__.deviceprofileId )
            url = "http://52.59.232.190/api/v1/device-profile/" + self.__class__.deviceprofileId  + "?" + "tenantId=" + "62e96b215ded5e474e2f035f"
            print(url)
            payload = {}
            response = requests.request("GET", url, headers=get_access_token(), data=payload)
            print(response)
            self.assertEqual(response.status_code, 200)
            json_path = os.path.join(os.path.dirname(__file__),'test_data', 'input', 'create_deviceprofile.json')
            with open(json_path) as json_file1:
                payload = json.load(json_file1)
                print(payload['name'])

            device_name = response.json()["data"]["name"]
            self.assertEqual(payload['name'], device_name)
            print("get tenant test case passed")

        except Exception as error:
            raise error

    def test_13_update_deviceprofile(self):
        try:
            print(self.__class__.deviceprofileId)
            url = "http://52.59.232.190/api/v1/device-profile?tenantId=62e96b215ded5e474e2f035f"
            json_path = os.path.join(os.path.dirname(__file__), 'test_data','input', 'update_deviceprofile.json')
            with open(json_path) as json_file:
                read_file = json.load(json_file)
            read_file["_id"] = self.__class__.deviceprofileId
            payload = json.dumps(read_file)

            print(payload)
            response = requests.request("PUT", url, headers=get_access_token(), data=payload)
            self.assertEqual(response.status_code, 200)
            print(response)
            self.assertEqual(response.json()["data"], "updated successfully!")
            print(" updated device profile successfully")

        except Exception as error:
            raise error

    def test_14_delete_deviceprofile(self):
        try:
            print(self.__class__.deviceprofileId)
            url = "http://52.59.232.190/api/v1/device-profile?tenantId=62e96b215ded5e474e2f035f"
            payload = json.dumps({
                "deviceProfileId":self.__class__.deviceprofileId })

            print(payload)

            response = requests.request("DELETE", url, headers=get_access_token(), data=payload)
            self.assertEqual(response.status_code, 200)
            print(response)
            self.assertEqual(response.json()["data"], "Deleted successfully!")
            print("device profile  successfully deleted")

        except Exception as error:
            raise error
