import unittest
from common import configuration
import os
import sys


def run(file_name=None, verbosity=2):
    print("Module Name: \n" + file_name)
    path = os.path.join(configuration.ROOT_PATH, 'jenkins-slave-tester1', 'docker_multi_build', 'tests')
    print("PATH: \n" + path)
    if os.path.exists(path):
        print("Path found\n")
    else:
        print("Path not found\n")
    if file_name is not None:
        # Only run the tests from the given module
        tests = unittest.TestLoader().discover(start_dir=os.path.join(configuration.ROOT_PATH, 'jenkins-slave-tester1', 'docker_multi_build', 'tests'),
                                               pattern=file_name, top_level_dir=configuration.ROOT_PATH)
    else:
        # run all the tests from all the test_* files
        tests = unittest.TestLoader().discover(start_dir=os.path.join(configuration.ROOT_PATH, 'jenkins-slave-tester1', 'docker_multi_build', 'tests'),
                                               pattern='test_*.py', top_level_dir=configuration.ROOT_PATH)

    print(tests)
    with open('./results.txt', 'w') as output:
        unittest.TextTestRunner(output, verbosity=verbosity).run(tests)
    print('completed')

    with open('./results.txt', 'r') as output:
        print(output.read())


if __name__ == "__main__":
    module_names = ['test_api.py', 'test_all.py']
    for module_name in module_names:
        result_file_name = "result_" + module_name.split('.')[0] + ".txt"
        path = str(configuration.ROOT_PATH + '\\tests' + '\\results\\' + result_file_name)
        print("Curent directory \n" + os.getcwd())
        print("Curent path \n" + path)
        run(file_name=module_name)

