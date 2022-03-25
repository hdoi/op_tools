# -*- coding: utf-8 -*-

from .context import op_tools

import unittest


def f_2(r):
    return r


class TestOp_py(unittest.TestCase):

    def test_nda_order_parameter(self):
        coord = [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0]]
        neighbor_list = [[1, 2], [0, 2], [0, 1]]
        box_length = [5 for i in range(3)]
        d_condition = {
            'ave_times': 1, 'o_factor': [0], 'oi_oj_ok': [0], 'func': [f_2]}
        thread_num = 1

        expected = {
            'a=1_f1=0_f2=0_f3=0': [1.4142135623730951, 1.4142135623730951, 1.4142135623730951],
            'a=0_f1=0_f2=0_f3=0': [1.4142135623730951, 1.4142135623730951, 1.4142135623730951]}

        actual = op_tools.op_d_nda.nda_order_parameter(
            coord, box_length, d_condition, neighbor_list, thread_num)

        self.assertEqual(expected, actual)

        coord = [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0]]
        neighbor_list = [[1, 2], [2], []]
        box_length = [5 for i in range(3)]
        d_condition = {
            'ave_times': 1, 'o_factor': [0], 'oi_oj_ok': [0], 'func': [f_2]}
        thread_num = 1

        expected = {'a=0_f1=0_f2=0_f3=0': [1.4142135623730951, 0, 0],
                    'a=1_f1=0_f2=0_f3=0': [0.47140452079103173, 0.0, 0.0]}

        actual = op_tools.op_d_nda.nda_order_parameter(
            coord, box_length, d_condition, neighbor_list, thread_num)
        self.assertEqual(expected, actual)
