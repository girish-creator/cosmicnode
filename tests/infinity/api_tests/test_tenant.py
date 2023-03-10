import unittest
import requests
import json
from utils import Tenant, LevelTemplates, LevelTypes, Level, \
    FactoryGateway, ControlApi, ZoneProfile


class TenantApiTests(unittest.TestCase):
    def setUp(self):
        self.tenant = Tenant()
        self.payload = {
            "businessName": "cosmic12",
            "image": "https://infopark.in/assets/image"
                     "s/slider/homeBanner1.jpg",
            "description": "Lorem ipsum dolor sit amet, consec"
                           "tetur adipiscing elit, sed do eiusmod tempor",
            "logo": "image.png",
            "businessTheme": "themeBlack",
            "url": "http://sdjksgdhsd"
        }

        self.tenant.create(self.payload)
        self.tenant_id = self.tenant.get_id()

    def tearDown(self):
        if self.tenant_id:
            self.tenant.delete(value=self.tenant_id)

    def test_create_tenant_not_admin(self):
        self.tenant.delete(value=self.tenant_id)
        response = self.tenant.create(payload=self.payload)
        self.assertEqual(response.status_code, 200)
        response_dict = response.json()["data"]

        self.assertEqual(self.payload['businessName'],
                         response_dict['businessName'])
        self.assertEqual(self.payload['image'],
                         response_dict['image'])
        self.assertEqual(self.payload['description'],
                         response_dict['description'])
        self.assertEqual(self.payload['logo'],
                         response_dict['logo'])
        self.assertEqual(self.payload['businessTheme'],
                         response_dict['businessTheme'])
        self.assertEqual(self.payload['url'],
                         response_dict['url'])

    def test_get_tenant_details(self):
        response = self.tenant.get_details(tenant_id=self.tenant_id)
        self.assertEqual(response.status_code, 200)
        response_dict = response.json()["data"]
        self.assertEqual(self.payload['businessName'],
                         response_dict['businessName'])

    def test_update_tenant_details(self):
        payload = {
            "businessName": "cosmicN",
            "image": "https://infopark.in/assets/image"
                     "s/slider/homeBanner1.jpg",
            "description": "text in description also updated",
            "tenantId": self.tenant_id
        }
        response = self.tenant.update(payload=payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["data"], "updated successfully!")

    def test_get_all_tenants(self):
        response = self.tenant.get_list(api='tenants')
        self.assertEqual(response.status_code, 200)

    def test_delete_tenant(self):
        response = self.tenant.delete(value=self.tenant_id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["data"], "Deleted successfully!")


if __name__ == '__main__':
    unittest.main()
