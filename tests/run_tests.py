"""Runs all relevant tests"""
import unittest
import os

from dantes_api.utils import path_utils


def main():
    dump_to_file = True
    # Load all the relevant tests
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTests(loader.discover(os.path.join(os.path.dirname(__file__), 'unit_tests'),
                                   top_level_dir=path_utils.get_project_root()))
    result_file_name = "results.txt"
    # Run all the tests that were loaded
    if dump_to_file:
        with open(result_file_name, 'w') as result_output_file:
            runner = unittest.TextTestRunner(result_output_file, verbosity=3)
            result = runner.run(suite)


if __name__ == '__main__':
    main()
