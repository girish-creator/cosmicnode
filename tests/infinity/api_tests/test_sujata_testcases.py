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
        print(access_token)
        return headers


    except Exception as error:
        raise error

class CloudApiTests(unittest.TestCase):
    tenantId=''
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_01_create_tenant(self):
        try:
            url = "http://52.59.232.190/api/v1/tenant"
            json_path = os.path.join(os.path.dirname(__file__), 'test_data', 'input', 'create_tenant_id.json')
            with open(json_path) as json_file:
                payload = json.dumps(json.load(json_file))
            response = requests.request("POST", url, headers=get_access_token(), data=payload)
            self.assertEqual(response.status_code, 200)
            response_dict = response.json()["data"]
            self.__class__.tenantId = response_dict["_id"]
            print(self.__class__.tenantId)
            keys_to_remove = ["children", "status", "_id",  "createdAt", "__v"]
            for key in keys_to_remove:
                response_dict.pop(key)
            validation_payload = json.loads(payload)
            self.assertEqual(response_dict, validation_payload)
            print("Tenant \" {} \" successfully created ".format(response_dict['businessName']))
            print("Test Passed!!!")

        except Exception as error:
            raise error

    def test_02_get_tenant(self):
        try:
            print(self.__class__.tenantId)
            url = "http://52.59.232.190/api/v1/tenant/" + self.__class__.tenantId
            payload = {}
            response = requests.request("GET", url, headers=get_access_token(), data=payload)
            self.assertEqual(response.status_code, 200)
            json_path = os.path.join(os.path.dirname(__file__), 'test_data', 'input', 'create_tenant_id.json')
            with open(json_path) as json_file1:
                payload = json.load(json_file1)
                print(payload['businessName'])
            business_name = response.json()["data"]["businessName"]
            self.assertEqual(payload['businessName'], business_name)
            print("get tenant test case passed")

        except Exception as error:
            raise error

    def test_03_update_tenant(self):
        try:
            print(self.__class__.tenantId)
            url = "http://52.59.232.190/api/v1/tenant"
            json_path = os.path.join(os.path.dirname(__file__), 'test_data', 'input', 'update_tenant.json')
            with open(json_path) as json_file:
                read_file= json.load(json_file)
                read_file["tenantId"] = self.__class__.tenantId
                payload = json.dumps(read_file)
            print(payload)
            response = requests.request("PUT", url, headers=get_access_token(), data=payload)
            self.assertEqual(response.status_code, 200)
            print(response)
            self.assertEqual(response.json()["data"], "updated successfully!")
            print("Tenant updated successfully")

        except Exception as error:
            raise error

    def test_04_get_tenant_update(self):

        try:
            print(self.__class__.tenantId)
            url = "http://52.59.232.190/api/v1/tenant/" + self.__class__.tenantId
            payload = {}
            response = requests.request("GET", url, headers=get_access_token(), data=payload)
            self.assertEqual(response.status_code, 200)
            json_path = os.path.join(os.path.dirname(__file__), 'test_data', 'input', 'update_tenant.json')
            with open(json_path) as json_file1:
                payload = json.load(json_file1)
                keys = ["businessName","image","description"]
                for key in keys:
                    updated_value = response.json()["data"][key]
                    print(updated_value)
                    self.assertEqual(payload[key], updated_value)
                print("get tenant test case passed after update")

        except Exception as error:
            raise error

    def test_05_getList_tenant(self):

        try:
            url = "http://52.59.232.190/api/v1/tenants"
            payload = {}
            response = requests.request("GET", url, headers=get_access_token(), data=payload)
            response_dict = response.json()["success"]
            print(response_dict)
            self.assertEqual(response.status_code, 200)
            print("status_code = 200")
            self.assertEqual(response_dict, True)
            print(response.json()["data"])

            print("Get tenant list test cases passed")

        except Exception as error:
            raise error

    def test_06_delete_tenant(self):

        try:
            print(self.__class__.tenantId)
            url = "http://52.59.232.190/api/v1/tenant/"
            payload = json.dumps({
                "tenantId": self.__class__.tenantId})
            response = requests.request("DELETE", url, headers=get_access_token(), data=payload)
            self.assertEqual(response.status_code, 200)
            print(response)
            self.assertEqual(response.json()["data"],"updated successfully!")
            print("Tenant deleted successfully")

        except Exception as error:
            raise error

    def test_07_create_channel(self):
        try:
            url = "http://52.59.232.190/api/v1/channel?tenantId=62e96b215ded5e474e2f035f"
            json_path = os.path.join(os.path.dirname(__file__),'test_data','input', 'create_channel.json')
            with open(json_path) as json_file:
                payload = json.dumps(json.load(json_file))
                print(payload)
            response = requests.request("POST", url, headers=get_access_token(), data=payload)
            self.assertEqual(response.status_code, 200)
            print(response.json()['data'])
            response_dict = response.json()["data"]
            self.__class__.channelId = response_dict["_id"]
            print(self.__class__.channelId)
            keys_to_remove = [ "status", "_id", "createdAt", "__v"]
            for key in keys_to_remove:
                response_dict.pop(key)
            validation_payload = json.loads(payload)
            self.assertEqual(response_dict, validation_payload)
            print("Channel \" {} \" successfully created ".format(response_dict['name']))
            print("Test Passed!!!")

        except Exception as error:
            raise error

    def test_08_update_channel(self):
        try:
            print(self.__class__.channelId)
            url = "http://52.59.232.190/api/v1/channel?tenantId=62e96b215ded5e474e2f035f"
            json_path = os.path.join(os.path.dirname(__file__),'test_data','input', 'update_channel.json')
            with open(json_path) as json_file:
                read_file = json.load(json_file)
            read_file["_id"] = self.__class__.channelId
            payload = json.dumps(read_file)

            print(payload)
            response = requests.request("PUT", url, headers=get_access_token(), data=payload)
            self.assertEqual(response.status_code, 200)
            print(response)
            self.assertEqual(response.json()["data"], "updated successfully!")
            print("channel updated successfully")

        except Exception as error:
            raise error

    def test_09_get_channel(self):
        try:
            subtenantId = "62e96b215ded5e474e2f035f"
            print(subtenantId)
            print(self.__class__.channelId)
            url = "http://52.59.232.190/api/v1/channel/" + self.__class__.channelId + "?" + "tenantId=" + "62e96b215ded5e474e2f035f"
            print(url)
            payload = {}
            response = requests.request("GET", url, headers=get_access_token(), data=payload)
            print(response)
            self.assertEqual(response.status_code, 200)
            response_dict = response.json()["data"]
            keys_to_remove = ["_id", "status"]
            for key in keys_to_remove:
                response_dict.pop(key)
                print(response_dict)

            json_path = os.path.join(os.path.dirname(__file__), 'test_data','input', 'update_channel.json')
            with open(json_path) as json_file1:
                payload = json.load(json_file1)
                print(payload)

            self.assertEqual(payload, response_dict)
            print("get channel test case passed")

        except Exception as error:
            raise error

    def test_10_getlist_delete_channel(self):
        try:
            url = "http://52.59.232.190/api/v1/channels/"
            payload = {}
            response = requests.request("GET", url, headers=get_access_token(), data=payload)
            list_of_channel = response.json()["data"]
            print(list_of_channel)
            count = 0
            for channel in list_of_channel:
                if channel["name"] == "channelupdated":
                    count += 1
                    url = "http://52.59.232.190/api/v1/channels/"
                    payload = json.dumps({
                        "channelId": channel["_id"]})
                    response = requests.request("DELETE", url, headers=get_access_token(), data=payload)
                print("Successfully deleted the site {}".format(channel["name"]))
            if count == 0:
                print("Channelupdated not found in the list of channels")
            else:
                print("Found {} site named channelupdated".format(count))
        except Exception as error:
            raise error

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

    def test_15_create_zoneprofile(self):
        try:
            url = "http://52.59.232.190/api/v1/zone-profile?tenantId=62e9669d5ded5e474e2f0281"
            print(url)
            json_path = os.path.join(os.path.dirname(__file__),'test_data','input', 'create_zoneprofile.json')
            with open(json_path) as json_file:
                payload = json.dumps(json.load(json_file))
                print(payload)
            response = requests.request("POST", url, headers=get_access_token(), data=payload)

            self.assertEqual(response.status_code, 200)
            print(response.json()['data'])
            response_dict = response.json()["data"]
            self.__class__.zoneprofileId = response_dict["_id"]
            print(self.__class__.zoneprofileId)
            keys_to_remove = ["status", "_id", "createdAt", "__v"]
            for key in keys_to_remove:
                response_dict.pop(key)
            validation_payload = json.loads(payload)
            self.assertEqual(response_dict, validation_payload)
            print("zone profile \" {} \" successfully created ".format(response_dict['name']))
            print("Test Passed!!!")

        except Exception as error:
            raise error

    def test_16_get_zoneprofile(self):
        try:

            print(self.__class__.zoneprofileId)
            url = "http://52.59.232.190/api/v1/zone-profile/" + self.__class__.zoneprofileId + "?" + "tenantId= 62e9669d5ded5e474e2f0281"
            print(url)
            payload = {}
            response = requests.request("GET", url, headers=get_access_token(), data=payload)
            print(response)
            self.assertEqual(response.status_code, 200)
            json_path = os.path.join(os.path.dirname(__file__),'test_data', 'input', 'create_zoneprofile.json')
            with open(json_path) as json_file1:
                payload = json.load(json_file1)
                print(payload['name'])

            zoneprofile_name = response.json()["data"]["name"]
            self.assertEqual(payload['name'], zoneprofile_name)
            print("get zone profile test case passed")

        except Exception as error:
            raise error

    def test_17_update_zoneprofile(self):
        try:
            print(self.__class__.zoneprofileId)
            url = "http://52.59.232.190/api/v1/zone-profile?tenantId=62e9669d5ded5e474e2f0281"
            json_path = os.path.join(os.path.dirname(__file__), 'test_data', 'input', 'update_zoneprofile.json')
            with open(json_path) as json_file:
                read_file = json.load(json_file)
            read_file["_id"] = self.__class__.zoneprofileId
            payload = json.dumps(read_file)

            print(payload)
            response = requests.request("PUT", url, headers=get_access_token(), data=payload)
            self.assertEqual(response.status_code, 200)
            print(response)
            self.assertEqual(response.json()['data'], "updated successfully!")
            print("zone-profile updated successfully")

        except Exception as error:
            raise error

    def test_18_delete_zoneprofile(self):
        try:
            print(self.__class__.zoneprofileId)
            url = "http://52.59.232.190/api/v1/zone-profile?tenantId=62e9669d5ded5e474e2f0281"
            payload = json.dumps({
                "zoneProfileId": self.__class__.zoneprofileId})
            response = requests.request("DELETE", url, headers=get_access_token(), data=payload)
            self.assertEqual(response.status_code, 200)
            print(response)
            self.assertEqual(response.json()["data"], "Deleted successfully!")
            print("zone profile successfully deleted")

        except Exception as error:
            raise error

if __name__ == '__main__':
    unittest.main()
