# -*- coding: utf-8 -*-

from .context import op_tools

import unittest
from math import sqrt


class TestOp_py(unittest.TestCase):

    def test_top_order_parameter(self):
        coord = [
            [0.0          , 0.0        , 0.0]  , 
            [ sqrt(8.0/9) , 0.0        , -1.0/3] , 
            [-sqrt(2.0/9) ,  sqrt(2.0/3)  , -1.0/3] , 
            [-sqrt(2.0/9) , -sqrt(2.0/3) , -1.0/3] , 
            [0          , 0          , 1]]
        neighbor_list = [[1, 2, 3, 4], [0, 2], [1, 3], [2, 4], [3, 0]]
        box_length = [5 for i in range(3)]
        c_condition = {'ave_times': 1, 'o_factor': [1], 'oi_oj_ok': [0]}
        thread_num = 1

        expected = {'a=0': [1.0, 0.5042091881014017, 0.7395833333333334, 0.7395833333333334, 0.5042091881014019],
                    'a=1': [0.6975170085738941, 0.7479308404782451, 0.6611252849226895, 0.6611252849226896, 0.7479308404782451]}

        actual = op_tools.op_i_top.top_order_parameter(
            coord, box_length, c_condition, neighbor_list, thread_num)

        self.assertEqual(expected, actual)
        
        # check 0 neighbor
        coord = [
            [0.0          , 0.0        , 0.0]  , 
            [ sqrt(8.0/9) , 0.0        , -1.0/3] , 
            [-sqrt(2.0/9) ,  sqrt(2.0/3)  , -1.0/3] , 
            [-sqrt(2.0/9) , -sqrt(2.0/3) , -1.0/3] , 
            [0          , 0          , 1]]
        neighbor_list = [[1, 2, 3, 4], [0, 2], [1, 3], [2], []]
        box_length = [5 for i in range(3)]
        c_condition = {'ave_times': 1, 'o_factor': [1], 'oi_oj_ok': [0]}
        thread_num = 1

        expected = {'a=0': [1.0, 0.5042091881014017, 0.7395833333333334, 1.0, 1.0], 'a=1': [0.8487585042869469, 0.7479308404782451, 0.747930840478245, 0.8697916666666667, 1.0]}

        actual = op_tools.op_i_top.top_order_parameter(
            coord, box_length, c_condition, neighbor_list, thread_num)
        self.assertEqual(expected, actual)
