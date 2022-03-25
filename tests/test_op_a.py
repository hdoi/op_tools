# -*- coding: utf-8 -*-

from .context import op_tools

import unittest


class TestOp_py(unittest.TestCase):

    def test_cnp_order_parameter(self):
        coord = [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0],
                 [0.0, 1.0, 0.0], [0.0, 0.5, 0.5], [0.5, 0.5, 0.5]]
        neighbor_list = [[1, 2, 3, 4], [0, 2, 3, 4], [
            0, 1, 3, 4], [0, 1, 2, 4], [0, 1, 2, 3]]
        box_length = [5.0 for i in range(3)]
        a_condition = {'ave_times': 1, 'm_in_A': [2], 'op_types': ['A']}
        thread_num = 1

        # CNP
        expected = {'a=0_type=A_m=2': [6.0, 6.0, 5.0, 4.0, 6.0],
                    'a=1_type=A_m=2': [5.4, 5.4, 5.4, 5.4, 5.4]}

        actual = op_tools.op_a_cnp.cnp_order_parameter(
            coord, box_length, a_condition, neighbor_list, thread_num)
        self.assertEqual(expected, actual)

        # PCNP
        a_condition['op_types'] = ['P']
        expected = {'a=0_type=P_m=2': [8.4375, 9.9375, 10.4375, 9.8125, 8.625],
                    'a=1_type=P_m=2': [9.45, 9.45, 9.45, 9.45, 9.45]}

        actual = op_tools.op_a_cnp.cnp_order_parameter(
            coord, box_length, a_condition, neighbor_list, thread_num)
        self.assertEqual(expected, actual)

        coord = [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0],
                 [0.0, 1.0, 0.0], [-1.0, 0.0, 0.0], [0.0, -1.0, 0.0]]
        neighbor_list = [[1, 2, 3, 4], [0, 2, 3, 4], [
            0, 1, 3, 4], [0, 1, 2, 4], [0, 1, 2, 3]]
        box_length = [5.0 for i in range(3)]
        a_condition = {'ave_times': 1, 'm_in_A': [2], 'op_types': ['N']}
        thread_num = 1

        # ACNP
        expected = {'a=0_type=N_m=2': [0.0, 31.25, 36.25, 25.25, 31.25],
                    'a=1_type=N_m=2': [24.8, 24.8, 24.8, 24.8, 24.8]}

        actual = op_tools.op_a_cnp.cnp_order_parameter(
            coord, box_length, a_condition, neighbor_list, thread_num)
        self.assertEqual(expected, actual)

        # check 0 neighbor test
        coord = [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0],
                 [0.0, 1.0, 0.0], [-1.0, 0.0, 0.0], [0.0, -1.0, 0.0]]
        neighbor_list = [[1, 2, 3, 4], [1, 2, 3], [3, 4], [4], []]
        box_length = [5.0 for i in range(3)]
        a_condition = {'ave_times': 1, 'm_in_A': [2], 'op_types': ['N']}
        thread_num = 1

        # ACNP
        expected = {'a=0_type=N_m=2': [0.0, 13.333333333333334, 5.0, 0.0, 0],
                    'a=1_type=N_m=2': [3.666666666666667, 7.916666666666668, 1.6666666666666667, 0.0, 0.0]}

        actual = op_tools.op_a_cnp.cnp_order_parameter(
            coord, box_length, a_condition, neighbor_list, thread_num)
        self.assertEqual(expected, actual)
