import unittest
import requests
import json
from utils import delete_site_level, get_payload_for_post_request, \
    get_access_token, create_site_level


class LevelApiTest(unittest.TestCase):
    def setUp(self):
        self.tenant_id = '62e516435213918b0f411246'
        self.url = "http://52.59.232.190/api/v1/level"

    def tearDown(self):
        if self.tenant_id:
            delete_site_level(self.url, self.tenant_id, "Grasrijk")

    def test_create_site_level(self):
        url = "http://52.59.232.190/api/v1/level"
        payload = get_payload_for_post_request('create_site_level')

        response = create_site_level(url, 'create_site_level')

        self.assertEqual(200, response.status_code)

        response_dict = response.json()["data"]

        self.tenant_id = response_dict['tenantId']

        payload = json.loads(payload)

        self.assertEqual(payload['levelTypeInfo'],
                         response_dict['levelTypeInfo'])
        self.assertEqual(payload['levelTypeId'],
                         response_dict['levelTypeId'])
        self.assertEqual(payload['tenantId'],
                         response_dict['tenantId'])
        self.assertEqual(payload['locationAddress'],
                         response_dict['locationAddress'])
        self.assertEqual(payload['geoLocation'],
                         response_dict['geoLocation'])
        self.assertEqual(payload['contact'],
                         response_dict['contact'])

    def test_get_site_level(self):
        response = create_site_level(self.url, 'create_site_level')
        res_dict = response.json()

        self.tenant_id = res_dict['data']['tenantId']

        url_with_tenant_id = f"{self.url}s?tenantId={self.tenant_id}"

        response = requests.request("GET", url_with_tenant_id,
                                    headers=get_access_token())

        list_of_levels = response.json()["data"]["levelList"]

        self.levels = [level for level in list_of_levels if (
                (level['tenantId'] == self.tenant_id) and
                (level["levelTypeInfo"]["name"] == "Grasrijk"))]

        self.assertEqual(len(self.levels), 1)

    def test_delete_site_level(self):
        response = create_site_level(self.url, 'create_site_level')
        res_dict = response.json()

        tenant_id = res_dict['data']['tenantId']

        delete_site_level(self.url, tenant_id, "Grasrijk")

        url_with_tenant_id = f"{self.url}s?tenantId={self.tenant_id}"

        response = requests.request("GET", url_with_tenant_id,
                                    headers=get_access_token())

        list_of_levels = response.json()["data"]["levelList"]

        levels = [level for level in list_of_levels if (
                (level['tenantId'] == self.tenant_id) and
                (level["levelTypeInfo"]["name"] == "Grasrijk"))]

        self.assertEqual(len(levels), 0)

    def test_get_all_level(self):
        x = Level()
        c = x.create_level()
        level_id = x.get_level_id()
        response_get_list = x.get_level_list()
        update_x = {
            "_id": level_id,
            "levelTypeInfo": {
                "name": "infopark-buildin",
                "image": "http://app.pundreek.com/cos/assets/fpl2.jpg",
                "description": "Lorem ipsum dolor sit amet, consectetu"
                               "r adipiscing elit, sed do eiusmod tempor"
            }
        }

        response_get_details = x.get_level_details()
        response = x.update_level(update_x)
        response_del = x.delete_level(level_type_id)
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
