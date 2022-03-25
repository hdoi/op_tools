# -*- coding: utf-8 -*-

from .context import op_tools

import unittest


class TestOp_py(unittest.TestCase):

    def test_aha_order_parameter(self):
        coord = [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0]]
        neighbor_list = [[1, 2], [0, 2], [0, 1]]
        box_length = [5 for i in range(3)]
        h_condition = {'ave_times': 1, 'b_in_H': 1, 'hist_num': [24], 'nu': [3]}
        thread_num = 1

        expected = {
            'a=0_b=0_bin=24_nu=3': [1.0, 1.0, 1.0],
            'a=0_b=1_bin=24_nu=3': [0.5555555555555554, 0.5555555555555554, 0.5555555555555554],
            'a=1_b=0_bin=24_nu=3': [1.0, 1.0, 1.0],
            'a=1_b=1_bin=24_nu=3': [0.5555555555555554, 0.5555555555555554, 0.5555555555555554]}
        actual = op_tools.op_h_aha.aha_order_parameter(coord, box_length, h_condition, neighbor_list, thread_num)
        self.assertEqual(expected, actual)

        # check 0 neighbor
        coord = [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0]]
        neighbor_list = [[1, 2], [0], []]
        box_length = [5 for i in range(3)]
        h_condition = {'ave_times': 1, 'b_in_H': 1, 'hist_num': [24], 'nu': [3]}
        thread_num = 1

        expected = {'a=0_b=0_bin=24_nu=3': [1.0, 1.0, 1.0],
                    'a=0_b=1_bin=24_nu=3': [0.1111111111111111, 0.0, 1.0],
                    'a=1_b=0_bin=24_nu=3': [1.0, 1.0, 1.0],
                    'a=1_b=1_bin=24_nu=3': [0.3703703703703704, 0.05555555555555555, 1.0]}
        actual = op_tools.op_h_aha.aha_order_parameter(coord, box_length, h_condition, neighbor_list, thread_num)
        self.assertEqual(expected, actual)
