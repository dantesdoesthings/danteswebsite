import os


ROOT_DIR = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))


def get_project_root() -> str:
    """Returns the location of the root directory of the project."""
    return ROOT_DIR


def get_tests_directory() -> str:
    """Returns the location of the tests directory."""
    return os.path.join(ROOT_DIR, 'tests')


def get_tests_data_directory() -> str:
    """Returns the location of the tests/data directory."""
    return os.path.join(ROOT_DIR, 'tests', 'data')
