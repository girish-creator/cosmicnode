import unittest
import requests
import json
import os


def get_access_token():
    try:
        login_url = "http://52.59.232.190/api/v1/login"
        login_payload = json.dumps({
            "email": "sd.cosmicnode@gmail.com", "password": "password"
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
