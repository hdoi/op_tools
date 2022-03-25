# -*- coding: utf-8 -*-

from .context import op_tools

import unittest


class TestOp_py(unittest.TestCase):

    def test_cpa_order_parameter(self):
        coord = [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [-1.0, 0.0, 0.0]]
        neighbor_list = [[1, 2], [0, 2], [0, 1]]
        box_length = [5 for i in range(3)]
        c_condition = {'ave_times': 1}
        thread_num = 1

        expected = {'a=0': [0.0, 9.0, 9.0],
                    'a=1': [6.0, 6.0, 6.0]}

        actual = op_tools.op_c_cpa.cpa_order_parameter(
            coord, box_length, c_condition, neighbor_list, thread_num)

        self.assertEqual(expected, actual)

        # check 0 neighbor
        coord = [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [-1.0, 0.0, 0.0]]
        neighbor_list = [[1, 2], [0], []]
        box_length = [5 for i in range(3)]
        c_condition = {'ave_times': 1}
        thread_num = 1

        expected = {'a=0': [0.0, 0, 0],
                    'a=1': [0.0, 0.0, 0.0]}

        actual = op_tools.op_c_cpa.cpa_order_parameter(
            coord, box_length, c_condition, neighbor_list, thread_num)
        self.assertEqual(expected, actual)
