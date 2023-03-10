import unittest
import requests
import json
from utils import LevelTypes


class FactoryGatewayApiTests(unittest.TestCase):
    def test_get_all_factory_gateway(self):
        x = FactoryGateway()
        c = x.create_factory_gateway()
        factory_gateway_id = x.get_factory_gateway_id()
        response_get_list = x.get_factory_gateway_list()
        update_x = {
            "_id": factory_gateway_id,
            "deviceAddress": 24512,
            "fwVersion": 2.1
        }

        response_get_details = x.get_factory_gateway_details()
        response = x.update_factory_gateway(update_x)
        response = x.delete_factory_gateway(factory_gateway_id)
        control_api = ControlApi()
        dummy_factory_data = {
            "identifier": "brightness_off",
            "tenantId": self.tenant_id,
            "levelId": self.level_id,
            "address": 32769,
            "onoff": 0
        }
        response = control_api.set_identifier(payload=dummy_factory_data)
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
