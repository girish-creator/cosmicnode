import sys
import unittest
import requests
import json
import os
sys.path.append(os.path.abspath(os.curdir))
sys.path.append(os.path.dirname(os.path.abspath(os.curdir)))
from source.utils import get_access_token



class ZoneProfileTests(unittest.TestCase):

    def test_15_create_zoneprofile(self):
        try:
            url = "http://52.59.232.190/api/v1/zone-profile?tenantId=62e9669d5ded5e474e2f0281"
            print(url)
            json_path = os.path.join(os.path.dirname(__file__),'test_data','input', 'create_zoneprofile.json')
            with open(json_path) as json_file:
                payload = json.dumps(json.load(json_file))
                print(payload)
            response = requests.request("POST", url, headers=get_access_token(), data=payload)
            print()
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
            raise

    def test_get_all_zone_profile(self):
        x = ZoneProfile()
        c = x.create_zone_profile()
        zone_profile_id = x.get_zone_profile_id()
        response_get_list = x.get_zone_profile_list()
        update_x = {
               "_id": zone_profile_id,
               "name": "meeting room",
               "controlType": "automatic",
               "sensor": {
                   "motion": {
                       "enabled": True,
                       "dimTime": 12,
                       "holdTime": 10
                   },
                   "daylight": {
                       "enabled": True,
                       "type": "ldr",
                       "ldrAdcThreshold": 3000,
                       "luxThreshold": 400,
                       "updateSteps": 2,
                       "updateInterval": 60
                   }
               },
               "powerOnLevel": 10,
               "maxLevel": 10
            }

        response_get_details = x.get_zone_profile_details()
        response_zone = x.update_zone_profile(update_x)
        response = x.delete_zone_profile(zone_profile_id)
        self.assertEqual(response.status_code, 200)







