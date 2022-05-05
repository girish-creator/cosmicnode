import unittest
from common import configuration
import os
import sys


def run(file_name=None, output=sys.stderr, verbosity=2):
    print("Module Name: \n" + file_name)
    path = os.path.join(configuration.ROOT_PATH, 'tests')
    print("PATH: \n" + path)
    if os.path.exists(path):
        print("Path found\n")
    else:
        print("Path not found\n")
    if file_name is not None:
        # Only run the tests from the given module
        tests = unittest.TestLoader().discover(start_dir=os.path.join(configuration.ROOT_PATH, 'tests'),
                                               pattern=file_name, top_level_dir=configuration.ROOT_PATH)
    else:
        # run all the tests from all the test_* files
        tests = unittest.TestLoader().discover(start_dir=os.path.join(configuration.ROOT_PATH, 'tests'),
                                               pattern='test_*.py', top_level_dir=configuration.ROOT_PATH)
    print(tests)
    unittest.TextTestRunner(output, verbosity=verbosity).run(tests)
    print('completed')


if __name__ == "__main__":
    module_names = ['test_api.py']
    for module_name in module_names:
        result_file_name = "result_" + module_name.split('.')[0] + ".txt"
        path = str(configuration.ROOT_PATH + '\\tests' + '\\results\\' + result_file_name)
        print("Curent directory \n" + os.getcwd())
        print("Curent path \n" + path)
        with open(path, 'w+') as file_obj:
            run(file_name=module_name, output=file_obj)

