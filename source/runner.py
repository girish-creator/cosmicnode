import unittest
import configuration
import os
import argparse
import sys


def run(file_name=None, verbosity=2):
    try:
        print("Module Name: \n" + file_name)

        if file_name is not None:
            # Only run the tests from the given module
            tests = unittest.TestLoader().discover(start_dir=os.path.join(configuration.ROOT_PATH, 'tests'),
                                                   pattern=file_name, top_level_dir=configuration.ROOT_PATH)
        else:
            # run all the tests from all the test_* files
            tests = unittest.TestLoader().discover(start_dir=os.path.join(configuration.ROOT_PATH, 'tests'),
                                                   pattern='test_*.py', top_level_dir=configuration.ROOT_PATH)

        print(tests)
        if os.path.exists('./results.txt'):
            os.remove('./results.txt')
        with open('./results.txt', 'a') as output:
            unittest.TextTestRunner(output, verbosity=verbosity).run(tests)

        print('completed')

        with open('./results.txt', 'r') as output:
            value = output.read()
            print(value)
            if 'FAILED (' in value:
                raise RuntimeError("Testcase failures or errors")
    except Exception as error:
        raise Exception(str.format("Test Runner Exception: {0}", error))


def verify_input_and_run(argument):
    try:
        run(file_name=argument + '.py')
    except Exception as error:
        raise Exception(str.format("Test Exception: {0}", error))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='CosmicNode Test Runner.')
    parser.add_argument('-test_file_name', metavar='test_file_name',
                        help='please provide test file name which you want to run.', default='')
    parser.add_argument('-test_list', nargs='+', metavar='test_list',
                        help='please provide a list of test files which you want to run.',
                        default='')

    args = parser.parse_args()

    if len(sys.argv) <= 1:
        sys.argv.append('--help')

    if args.test_file_name:
        verify_input_and_run(args.test_file_name)

    if args.test_list:
        for test_name in args.test_list:
            verify_input_and_run(test_name)

