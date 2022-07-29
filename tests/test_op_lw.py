# -*- coding: utf-8 -*-

from .context import op_tools

import unittest


class TestOp_py(unittest.TestCase):

    def test_spherical_order_parameter(self):
        # hcp crystal structure
        coord = [
            [0.0, 0.0, 0.0],
            [1.0, 0.0, 0.0],
            [0.5, 3**0.5 / 2.0, 0.0],
            [-0.5, 3**0.5 / 2.0, 0.0],
            [-1.0, 0.0, 0.0],
            [-0.5, -3**0.5 / 2.0, 0.0],
            [0.5, -3**0.5 / 2.0, 0.0],
            [0.0,  1.0 / (3**(0.5)), 2.0**(0.5) / 3.0**(0.5)],
            [0.5, -1.0 / (12**0.5), 2.0**(0.5) / 3.0**(0.5)],
            [-0.5, -1.0 / (12**0.5), 2.0**(0.5) / 3.0**(0.5)],
            [0.0,  1.0 / (3**(0.5)), -2.0**(0.5) / 3.0**(0.5)],
            [0.5, -1.0 / (12**0.5), -2.0**(0.5) / 3.0**(0.5)],
            [-0.5, -1.0 / (12**0.5), -2.0**(0.5) / 3.0**(0.5)]]
        neighbor_list = [[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], [
            0], [1], [2], [3], [4], [5], [6], [7], [8], [9], [10], [11], [12]]

        box_length = [5 for i in range(3)]
        q_condition = {'ave_times': 0, 'b_in_Q': 0, 'l_in_Q': [4, 6]}
        thread_num = 1

        expected = {'l=4_a=0_b=0': [0.1340970468803, 0.1340970468803,
                                    -0.05710227105471, -0.05710227105471, -0.05710227105471,
                                    -0.05710227105471, -0.05710227105471, 0.0298985047194,
                                    0.00060096490895, -0.05710227105471, -0.02943461720731,
                                    -0.02943461720731, -0.05710227105471],
                    'l=6_a=0_b=0': [0.03956384878849, 0.0397296604593,
                                    0.09171254590932, 0.09171254590932, 0.09171254590932,
                                    0.09171254590932, 0.09171254590932, -0.0706938930556,
                                    -0.0511840662213, 0.09171254590932, -0.06422604353072,
                                    -0.06422604353072, 0.09171254590932]}
        actual = op_tools.op_lqw_spherical.w_order_parameter(
            coord, box_length, q_condition, neighbor_list, thread_num)
        self.assertEqual(expected, actual)

        # check 0 neighbor
        coord = [
            [0.0, 0.0, 0.0],
            [1.0, 0.0, 0.0],
            [0.5, 3**0.5 / 2.0, 0.0]]
        neighbor_list = [[], [], []]
        box_length = [5 for i in range(3)]
        q_condition = {'ave_times': 0, 'b_in_Q': 0, 'l_in_Q': [4, 6]}
        thread_num = 1

        expected = {'l=4_a=0_b=0': [0.0, 0.0, 0.0],
                    'l=6_a=0_b=0': [0.0, 0.0, 0.0]}
        actual = op_tools.op_lqw_spherical.w_order_parameter(
            coord, box_length, q_condition, neighbor_list, thread_num)
        self.assertEqual(expected, actual)
