# -*- coding: utf-8 -*-

from .context import op_tools

import unittest


class TestOp_py(unittest.TestCase):

    """ test method of cnp """

    def test_onsager_order_parameter(self):
        neighbor_list = [[1, 2], [0, 2], [0, 1]]
        direct = [[1, 0, 0], [1, 0, 0], [1, 0, 0]]
        setting = {'ave_times': 1, 'n_in_S': [2, 4]}

        expected = {'a=0_n=2': [1.0, 1.0, 1.0],
                    'a=0_n=4': [1.0, 1.0, 1.0],
                    'a=1_n=2': [1.0, 1.0, 1.0],
                    'a=1_n=4': [1.0, 1.0, 1.0]}

        actual = op_tools.op_s_local_onsager.onsager_order_parameter(
            direct, setting, neighbor_list, 1)
        self.assertEqual(expected, actual)

        # check 0 neighbor
        neighbor_list = [[], [], [1]]
        direct = [[1, 0, 0], [1, 0, 0], [1, 0, 0]]
        setting = {'ave_times': 1, 'n_in_S': [2, 4]}

        expected = {'a=0_n=2': [0.0, 0.0, 1.0],
                    'a=0_n=4': [0.0, 0.0, 1.0],
                    'a=1_n=2': [0.0, 0.0, 0.5],
                    'a=1_n=4': [0.0, 0.0, 0.5]}

        actual = op_tools.op_s_local_onsager.onsager_order_parameter(
            direct, setting, neighbor_list, 1)
        self.assertEqual(expected, actual)
