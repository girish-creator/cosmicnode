import sys
import unittest
import requests
import json
import os
sys.path.append(os.path.abspath(os.curdir))
sys.path.append(os.path.dirname(os.path.abspath(os.curdir)))
from source.utils import get_access_token


class ChannelTests(unittest.TestCase):

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
