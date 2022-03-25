# -*- coding: utf-8 -*-

from .context import op_tools

import unittest


class TestOp_py(unittest.TestCase):

    def test_baa_order_parameter(self):
        coord = [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0]]
        neighbor_list = [[1, 2], [0, 2], [0, 1]]
        box_length = [5 for i in range(3)]
        b_condition = {'ave_times': 1, 'm': [1], 'phi': [0], 'n': [1]}
        thread_num = 1

        expected = {
            'a=0_m=1_phi=0_n=1': [6.123233995736766e-17, 0.7071067811865475, 0.7071067811865475],
            'a=1_m=1_phi=0_n=1': [0.4714045207910316, 0.4714045207910316, 0.4714045207910316]}
        actual = op_tools.op_b_baa.baa_order_parameter(
            coord, box_length, b_condition, neighbor_list, thread_num)
        self.assertEqual(expected, actual)

        # check 0 neighbors
        coord = [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0]]
        neighbor_list = [[1, 2], [0], []]
        box_length = [5 for i in range(3)]
        b_condition = {'ave_times': 1, 'm': [1], 'phi': [0], 'n': [1]}
        thread_num = 1

        expected = {'a=0_m=1_phi=0_n=1': [6.123233995736766e-17, 0, 0],
                    'a=1_m=1_phi=0_n=1': [2.041077998578922e-17, 3.061616997868383e-17, 0.0]}
        actual = op_tools.op_b_baa.baa_order_parameter(
            coord, box_length, b_condition, neighbor_list, thread_num)
        self.assertEqual(expected, actual)
