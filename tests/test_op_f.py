# -*- coding: utf-8 -*-

from .context import op_tools

import unittest


def f_1(r):
    return 1


class TestOp_py(unittest.TestCase):

    def test_afs_order_parameter(self):
        coord = [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0]]
        nei_list = [[1, 2], [0, 2], [0, 1]]
        box_length = [5.0 for i in range(3)]
        f_condition = {'ave_times': 1, 'oi_oj_ok': [0], 'o_factor': [0],
                       'func': [f_1], 'l_in_F': [0]}
        thread_num = 1

        expected = {'a=0_f1=0_f2=0_l=0': [1.0, 1.0, 1.0],
                    'a=1_f1=0_f2=0_l=0': [1.0, 1.0, 1.0], }
        actual = op_tools.op_f_afs.afs_order_parameter(
            coord, box_length, f_condition, nei_list, thread_num)
        self.assertEqual(expected, actual)

        # check 0 neighbor
        coord = [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0]]
        nei_list = [[1, 2], [0], []]
        box_length = [5.0 for i in range(3)]
        f_condition = {'ave_times': 1, 'oi_oj_ok': [0], 'o_factor': [0],
                       'func': [f_1], 'l_in_F': [0]}
        thread_num = 1

        expected = {'a=0_f1=0_f2=0_l=0': [1.0, 0, 0],
                    'a=1_f1=0_f2=0_l=0': [0.3333333333333333, 0.5, 0.0]}
        actual = op_tools.op_f_afs.afs_order_parameter(
            coord, box_length, f_condition, nei_list, thread_num)
        self.assertEqual(expected, actual)
