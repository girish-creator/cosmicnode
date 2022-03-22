import unittest
import configuration
import os
import sys


def run(file_name=None, output=sys.stderr, verbosity=2):
    if file_name is not None:
        # Only run the tests from the given module
        tests = unittest.TestLoader().discover(start_dir=os.path.join(configuration.ROOT_PATH, 'tests'),
                                               pattern=file_name, top_level_dir=configuration.ROOT_PATH)
    else:
        # run all the tests from all the test_* files
        tests = unittest.TestLoader().discover(start_dir=os.path.join(configuration.ROOT_PATH, 'tests'),
                                               pattern='test_*.py', top_level_dir=configuration.ROOT_PATH)
    unittest.TextTestRunner(output, verbosity=verbosity).run(tests)


if __name__ == "__main__":
    module_names = ['test_android_api.py', 'test_api.py']
    for module_name in module_names:
        result_file_name = "result_" + module_name.split('.')[0] + ".txt"
        with open(os.path.join(configuration.ROOT_PATH, 'tests', 'results', result_file_name), 'w+') as file_obj:
            run(file_name=module_name, output=file_obj)

