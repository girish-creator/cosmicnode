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

    def test_01_create_assetProfile(self):

        try:
            url = "http://52.59.232.190/api/v1/asset-profile?tenantId=62e4f3205213918b0f410f58"
            json_path = os.path.join(os.path.dirname(__file__), 'test_data', 'input', 'create_assetProfile.json')
            with open(json_path) as json_file:
                payload = json.dumps(json.load(json_file))
                print(payload)
            response = requests.request("POST", url, headers=get_access_token(), data=payload)
            with open(json_path) as json_file:
                payload1 = json.load(json_file)
            response_dict = response.json()["data"]["name"]
            print(response_dict)
            print(payload1["name"])
            if payload1["name"] == response_dict:
                print("success-full")
            self.assertEqual(response.status_code, 200)
            print("AssetProfile added successfully")

        except Exception as error:
            raise error

    def test_02_getById_assetProfile(self):

        try:
            url = "http://52.59.232.190/api/v1/asset-profile/62ebc31a02ad9e3139ec5c1a?tenantId=62e4f3205213918b0f410f58"
            payload = {}
            response = requests.request("GET", url, headers=get_access_token(), data=payload)
            response_dict = response.json()["data"]["name"]
            json_path = os.path.join(os.path.dirname(__file__), 'test_data', 'input', 'create_assetProfile.json')
            with open(json_path) as json_file:
                payload = json.load(json_file)
                print(payload)
            self.assertEqual(payload['name'], response_dict)
            print("getById of assetProfile was successfull")

        except Exception as error:
            raise error

    def test_03_update_assetProfile(self):

        try:
            url = "http://52.59.232.190/api/v1/asset-profile?tenantId=62e4f3205213918b0f410f58"
            json_path = os.path.join(os.path.dirname(__file__), 'test_data', 'input', 'update_assetProfile.json')
            with open(json_path) as json_file:
                payload = json.dumps(json.load(json_file))
            response = requests.request("PUT", url, headers=get_access_token(), data=payload)
            response_dict = response.json()["data"]
            self.assertEqual(response_dict, "updated successfully!")
            print("AssetProfile is successfully updated")

        except Exception as error:
            raise error

    def test_04_getList_assetProfile(self):

        try:
            url = "http://52.59.232.190/api/v1/asset-profiles?tenantId=62e4f3205213918b0f410f58"
            payload = {}
            response = requests.request("GET", url, headers=get_access_token(), data=payload)
            response_dict = response.json()["success"]
            self.assertEqual(response.status_code, 200)
            print("status_code = 200")
            self.assertEqual(response_dict, True)
            print("successfully listed")

        except Exception as error:
            raise error

    def test_05_delete_assetProfile(self):

        try:
            url = "http://52.59.232.190/api/v1/asset-profile?tenantId=62e4f3205213918b0f410f58"
            json_path = os.path.join(os.path.dirname(__file__), 'test_data', 'input', 'delete_assetProfile.json')
            with open(json_path) as json_file:
                payload = json.dumps(json.load(json_file))
            response = requests.request("DELETE", url, headers=get_access_token(), data=payload)
            response_dict = response.json()["data"]
            self.assertEqual(response_dict, "Deleted successfully!")
            print("AssetProfile was deleted successfully")

        except Exception as error:
            raise error