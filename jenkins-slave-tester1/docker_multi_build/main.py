# start running all the tests and generate a report for each and every test with a final consolidated report.
# store the reports and results in volume shared with the host.
# generated pass or fail criteria for each test and consolidated tests.
# return true or false to the jenkins server to set the job to pass or fail.
import unittest
import requests
import os
from common import configuration


class Test(unittest.TestCase):

    def test_write_csv_file(self):
        r = requests.get("https://chercher.tech/sample/api/product/read?id=90")
        print(r.json())
        print(r.status_code)
        x = self.assertEquals(r.status_code, 200)
        y = self.assertEquals(r.json(), [{'id': '90', 'name': None, 'description': None, 'price': None}])
        print(x)
        print(y)

        with open('test.txt', 'w') as f:
            f.write(str(r.json()))


if __name__ == "__main__":
    root_dir = os.path.abspath(os.getcwd())
    configuration.ROOT_PATH = root_dir
    unittest.main()