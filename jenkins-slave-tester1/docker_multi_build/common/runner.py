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
    module_name = 'test_android_api.py'
    with open(os.path.join(configuration.ROOT_PATH, 'tests', 'results', 'test_all.txt'), 'w+') as file_obj:
        run(output=file_obj)

