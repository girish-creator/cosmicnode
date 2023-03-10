import unittest
import requests
import json
from utils import LevelTypes


class LevelTypeApiTests(unittest.TestCase):
    def test_get_all_level_types(self):
        x = LevelTypes()
        c = x.create_level_type()
        level_type_id = x.get_level_type_id()
        response_get_list = x.get_level_type_list()
        update_x = {
            "_id": level_type_id,
            "type": "site",
            "field": [
                {
                    "type": "text",
                    "name": "name",
                    "validationmessage": "Name is required",
                    "label": "Name",
                    "required": True
                },
                {
                    "type": "textarea",
                    "name": "description",
                    "validationmessage": "Description is required",
                    "label": "description",
                    "required": True
                },
                {
                    "type": "file",
                    "name": "image",
                    "validationmessage": "Image is required",
                    "label": "Image",
                    "required": True
                }
            ]
        }

        response_get_details = x.get_level_template_details()
        response = x.update_level_type(update_x)
        response_del = x.delete_level_type(level_type_id)
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
