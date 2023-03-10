import unittest
import requests
import json
from utils import LevelTypes


class LevelTemplateApiTests(unittest.TestCase):
    def test_get_all_level_templates(self):
        x = LevelTemplates()
        c = x.create_level_template()
        level_template_id = x.get_level_template_id()
        response_get_list = x.get_level_template_list()
        update_x = {
            "_id": level_template_id,
            "businessTypeName": "template2",
            "status": "active"
        }

        response_get_details = x.get_level_template_details()
        response = x.update_level_template(update_x)
        response = x.delete_level_template(level_template_id)
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
