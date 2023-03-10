import unittest
import requests
import json
import os


def get_access_token():
    try:
        login_url = "http://52.59.232.190/api/v1/login"
        login_payload = json.dumps({
            "email": "platform-owner@cosmicnode.com", "password": "password"
        })
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", login_url, headers=headers, data=login_payload)
        access_token = {"accessToken": response.json()["data"]["accessToken"]}
        headers.update(access_token)
        return headers

    except Exception as error:
        raise error


class CloudApiTests(unittest.TestCase):
    tenantId = '62e4f3205213918b0f410f58'

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_01_create_site_level(self):
        try:
            url = "http://52.59.232.190/api/v1/level"
            json_path = os.path.join(os.path.dirname(__file__), 'test_data', 'input', 'create_site_level.json')
            with open(json_path) as json_file:
                payload = json.dumps(json.load(json_file))
            response = requests.request("POST", url, headers=get_access_token(), data=payload)
            self.assertEqual(200, response.status_code)
            response_dict = response.json()["data"]
            keys_to_remove = ["children", "status", "_id", "plan", "createdAt", "__v"]
            for key in keys_to_remove:
                response_dict.pop(key)
            validation_payload = json.loads(payload)
            self.assertEqual(response_dict, validation_payload)
            print("Level \" {} \" successfully created ".format(response_dict['levelTypeInfo']['name']))
            print("Test Passed!!!")
        except Exception as error:
            raise error

    def test_02_get_site_level(self):
        try:
            url = "http://52.59.232.190/api/v1/levels?tenantId=62e516435213918b0f411246"
            payload = {}
            response = requests.request("GET", url, headers=get_access_token(), data=payload)
            list_of_levels = response.json()["data"]["levelList"]
            count = 0
            for level in list_of_levels:
                if level["levelTypeInfo"]["name"] == "Grasrijk":
                    count += 1
                    url = "http://52.59.232.190/api/v1/level/?tenantId=62e516435213918b0f411246"
                    payload = json.dumps({
                        "levelId": level["_id"]})
                    response = requests.request("DELETE", url, headers=get_access_token(), data=payload)
                    print("Successfully deleted the site {}".format(level["levelTypeInfo"]["name"]))
            if count == 0:
                print("Site Grasrijk not found in the list of levels")
            else:
                print("Found {} site named Grasrijk".format(count))
        except Exception as error:
            raise error

    tenantId = '62e4f3205213918b0f410f58'

    def test_01_create_dataProperties(self):
        try:
            url = "http://52.59.232.190/api/v1/data-property?tenantId=62e4f3205213918b0f410f58"
            json_path = os.path.join(os.path.dirname(__file__), 'test_data', 'input', 'create_dataProperties.json')
            with open(json_path) as json_file:
                payload = json.dumps(json.load(json_file))
            response = requests.request("POST", url, headers=get_access_token(), data=payload)
            print(response.content)
            response_dict = response.json()["data"]

            keys_to_remove = ["status", "_id", "createdAt", "__v"]
            for key in keys_to_remove:
                response_dict.pop(key)
            print(response_dict)
            validation_payload = json.loads(payload)
            print(validation_payload)

            if response_dict == validation_payload:
                print("dataProperty  successfully created ")
                print("Test Passed!!!")

        except Exception as error:
            raise error

    def test_02_getById_dataProperties(self):
        try:
            print(self.__class__.tenantId)
            url = "http://52.59.232.190/api/v1/data-property/62ea34fc5ded5e474e2f0cf5?tenantId=62e4f3205213918b0f410f58"
            payload = {}
            response = requests.request("GET", url, headers=get_access_token(), data=payload)
            self.assertEqual(response.status_code, 200)
            json_path = os.path.join(os.path.dirname(__file__), 'test_data', 'input', 'create_dataProperties.json')
            with open(json_path) as json_file:
                payload = json.load(json_file)
                print(payload["name"])
            response_name = response.json()["data"]["name"]
            print(response_name)
            self.assertEqual(payload["name"], response_name)
            print("getById of dataProperties was success")

        except Exception as error:
            raise error

    def test_03_update_dataProperties(self):
        try:
            url = "http://52.59.232.190/api/v1/data-property?tenantId=62e4f3205213918b0f410f58"
            json_path = os.path.join(os.path.dirname(__file__), 'test_data', 'input', 'update_dataProperties.json')
            with open(json_path) as json_file:
                payload = json.dumps(json.load(json_file))
                print(payload)
            response = requests.request("PUT", url, headers=get_access_token(), data=payload)
            payload_dict = response.json()["data"]
            print(payload_dict)
            self.assertEqual(payload_dict, "updated successfully!")
            print("dataProperties is successfully updated")

        except Exception as error:
            raise error

    def test_04_delete_dataProperties(self):

        try:
            url = "http://52.59.232.190/api/v1/data-property?tenantId=62e4f3205213918b0f410f58"
            json_path = os.path.join(os.path.dirname(__file__), 'test_data', 'input', 'delete_dataProperties.json')
            with open(json_path) as json_file:
                payload = json.dumps(json.load(json_file))
                print(payload)
            response = requests.request("DELETE", url, headers=get_access_token(), data=payload)
            self.assertEqual(response.json()["data"], "Deleted successfully!")
            print("dataProperties was successfully deleted")

        except Exception as error:
            raise error

    def test_05_getList(self):

        try:
            url = "http://52.59.232.190/api/v1/data-properties?tenantId=62e4f3205213918b0f410f58"
            payload = {}
            response = requests.request("GET", url, headers=get_access_token(), data=payload)
            response_dict = response.json()["success"]
            self.assertEqual(response.status_code, 200)
            print("status_code = 200")
            self.assertEqual(response_dict, True)
            print("successfully listed")

        except Exception as error:
            raise error
