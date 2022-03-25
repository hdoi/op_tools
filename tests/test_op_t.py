# -*- coding: utf-8 -*-

from .context import op_tools

import unittest


class TestOp_py(unittest.TestCase):

    """ test method of cnp """

    def test_mcmillan_order_parameter(self):
        coord = [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0]]
        neighbor_list = [[1, 2], [0, 2], [0, 1]]
        direct = [[0, 0, 1], [0, 0, 1], [0, 0, 1]]
        box_length = [5.0 for i in range(3)]
        t_condition = {'ave_times': 1, 'oi_oj': [
            0], 'o_factor': [1], 'd_in_T': [1.00], 'n_in_T': [2, 4]}
        thread_num = 1

        expected = {'a=0_n=2_z=1.0': [1.0, 1.0, 1.0],
                    'a=1_n=2_z=1.0': [1.0, 1.0, 1.0],
                    'a=0_n=4_z=1.0': [1.0, 1.0, 1.0],
                    'a=1_n=4_z=1.0': [1.0, 1.0, 1.0]}

        actual = op_tools.op_t_msigma.mcmillan_order_parameter(
            coord, direct, box_length, t_condition, neighbor_list, thread_num)

        self.assertEqual(expected, actual)

        # check 0 neighbor
        coord = [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0]]
        neighbor_list = [[], [], []]
        direct = [[0, 0, 1], [0, 0, 1], [0, 0, 1]]
        box_length = [5.0 for i in range(3)]
        t_condition = {'ave_times': 1, 'oi_oj': [
            0], 'o_factor': [1], 'd_in_T': [1.00], 'n_in_T': [2, 4]}
        thread_num = 1

        expected = {'a=0_n=2_z=1.0': [0.0, 0.0, 0.0],
                    'a=0_n=4_z=1.0': [0.0, 0.0, 0.0],
                    'a=1_n=2_z=1.0': [0.0, 0.0, 0.0],
                    'a=1_n=4_z=1.0': [0.0, 0.0, 0.0]}

        actual = op_tools.op_t_msigma.mcmillan_order_parameter(
            coord, direct, box_length, t_condition, neighbor_list, thread_num)
        self.assertEqual(expected, actual)
