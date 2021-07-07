import unittest
import json
import os

import numpy as np

from dantes_api.data_generator import data_generation
from dantes_api.utils import path_utils


class TestTemplate(unittest.TestCase):

    def setUp(self):
        pass

    def test_data_generation(self):
        test_input = np.array(
            [[10, 10],
             [20, 15],
             [30, 10],
             [40, 25]]).T
        graph_range = [0, 70, 0, 50]
        res = np.array(data_generation.generate_natural_cubic_spline_data(test_input, graph_range, 10))
        with open(os.path.join(path_utils.get_tests_data_directory(), 'generated_data_1.json'), 'r') as json_file:
            expected = np.array(json.load(json_file))
        for r, e in zip(res, expected):
            self.assertTrue(np.all(np.isclose(r, e)))

