import unittest
import configuration
import os
import argparse
import sys


def run(file_name=None, start_directory=None, verbosity=2):
    """
    Runs a test file based on the file_name param. It uses unittest's
    test loader discovery module to find the location of the file_name
    provided using start_directory.

    :param file_name: name of the test file to be executed
    :param start_directory: path of the starting directory
    :param verbosity: level of readiness for the user to understand the issue.

    """
    try:
        if start_directory is None:
            start_directory = os.path.join(configuration.ROOT_PATH, 'tests')

        print(f"Test File:                  {file_name}")
        print(f"Test File start_directory:  {start_directory}")

        if file_name is not None:
            # Only run the tests from the given directory
            tests = unittest.TestLoader().discover(
                start_dir=start_directory,
                pattern=file_name)
        else:
            # run all the tests from all the test_* files
            tests = unittest.TestLoader().discover(
                start_dir=os.path.join(configuration.ROOT_PATH, 'tests'),
                pattern='test_*.py', top_level_dir=configuration.ROOT_PATH)

        if tests.countTestCases() == 0:
            print(f"No tests to execute in the given test file: {file_name}")
        else:
            print(f"Number of tests to execute: {tests.countTestCases()}")

            if os.path.exists('./results.txt'):
                os.remove('./results.txt')
            with open('./results.txt', 'a') as output:
                unittest.TextTestRunner(output,
                                        verbosity=verbosity).run(tests)

            with open('./results.txt', 'r') as output:
                value = output.read()
                print(value)

            with open('./results.txt', 'r') as output:
                value = output.read()
                print(value)
                if 'FAILED (' in value:
                    raise RuntimeError("Testcase failures or errors")

            print(f"Executed: {tests.countTestCases()} tests from "
                  f"{file_name}")

    except Exception as error:
        raise Exception(str.format("Test Runner Exception: {0}", error))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='CosmicNode Test Runner.')
    parser.add_argument('-test_file_name', metavar='test_file_name',
                        help="""please provide test file name which 
                        you want to run""", required=False)
    parser.add_argument('-product', metavar='product',
                        help="""please provide the product name for which 
                        you want to run the tests""", required=True)
    parser.add_argument('-type_of_tests', metavar='type_of_tests',
                        help="""please provide the type of the tests 
                        for the current product""", required=False)

    args = parser.parse_args()

    if args.product is None:
        raise RuntimeError("Please check the options for running this "
                           "file using new_runner.py --help")
    else:
        products = {'infinity': ['api_tests', 'all'],
                    'modbus': ['modbus_tests', 'api_tests', 'all'],
                    'gateway': ['api_tests', 'all']}

        path = os.getcwd()

        if args.product in products.keys():
            product_path = os.path.join(path, 'tests', args.product)

            if args.type_of_tests is None:
                print(f"Product:        '{args.product}'\n"
                      f"TestType:       'All'\n"
                      f"TestFile:       'All'\n")
                for root, dirs, files in os.walk(product_path):
                    for test_file_name in files:
                        if (test_file_name.startswith("test_")) and (
                                test_file_name.endswith(".py")):
                            test_file_path = os.path.join(root,
                                                          test_file_name)
                            run(test_file_name, root)

            elif args.type_of_tests in products[args.product]:
                test_type_path = os.path.join(product_path,
                                              args.type_of_tests)
                if args.test_file_name is None:
                    print(f"Product:        '{args.product}'\n"
                          f"TestType:       '{args.type_of_tests}'\n"
                          f"TestFile:       'All'\n")
                    for root, dirs, files in os.walk(test_type_path):
                        for test_file_name in files:
                            if test_file_name.startswith("test_"):
                                test_file_path = os.path.join(test_type_path,
                                                              test_file_name)
                                run(test_file_name, test_type_path)
                else:
                    print(f"Product:        '{args.product}'\n"
                          f"TestType:       '{args.type_of_tests}'\n"
                          f"TestFile:       '{args.test_file_name}'\n")
                    for root, dirs, files in os.walk(test_type_path):
                        for test_file_name in files:
                            test_file = test_file_name.split('.')[0]
                            if args.test_file_name == test_file:
                                test_file_path = os.path.join(test_type_path,
                                                              test_file_name)
                                run(test_file_name, test_type_path)
                                break
                        break
            else:
                print(f"type of test: '{args.type_of_tests}' for "
                      f"product: '{args.product}' does not exist")

        else:
            raise RuntimeError(f"Given product '{args.product}' does "
                               f"not exists in our products list "
                               f"{products.keys()}")
