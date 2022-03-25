# -*- coding: utf-8 -*-

from .context import op_tools

import unittest

import numpy as np


def f1(j, voronoi_area_list, distance_list):
    weight = 1.0/float(len(distance_list))
    return weight


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
            2], [1], [2], [3], [4], [5], [6], [7], [8], [9], [10], [11], [12]]

        box_length = [5 for i in range(3)]
        q_condition = {'ave_times': 0, 'oi_oj': [0], 'o_factor': [
            0], 'b_in_Q': 0, 'l_in_Q': [4, 6], 'p_in_Q': [0]}
        thread_num = 1

        expected = {'l=4_a=0_b=0': [0.28912440907390397, 0.9999999999999999, 0.9999999999999999, -0.28906250000000044, -0.2890625000000001, -0.2890624999999995, -0.2890625000000001, 0.09288194444444468, 0.02343750000000022, -0.28906250000000006, 0.13965650826446324, 0.13965650826446285, -0.28906250000000006],
                    'l=6_a=0_b=0': [0.5796795183469841, 0.9999999999999999, 0.9999999999999999, 0.32324218749999994, 0.3232421875000001, 0.32324218750000033, 0.3232421875000001, 0.10601128472222207, -0.3740234374999998, 0.3232421875000001, 0.047996836260330154, 0.04799683626033061, 0.3232421875000001]}

        actual = op_tools.op_lqw_spherical.spherical_order_parameter(
            coord, box_length, q_condition, neighbor_list, thread_num)
        self.assertEqual(expected, actual)

        # check 0 neighbor
        coord = [
            [0.0, 0.0, 0.0],
            [1.0, 0.0, 0.0],
            [0.5, 3**0.5 / 2.0, 0.0]]
        neighbor_list = [[], [], []]

        box_length = [5 for i in range(3)]
        q_condition = {'ave_times': 0, 'oi_oj': [0], 'o_factor': [
            0], 'b_in_Q': 0, 'l_in_Q': [4, 6], 'p_in_Q': [0]}
        thread_num = 1

        expected = {'l=4_a=0_b=0': [0.0, 0.0, 0.0],
                    'l=6_a=0_b=0': [0.0, 0.0, 0.0]}
        actual = op_tools.op_lqw_spherical.spherical_order_parameter(
            coord, box_length, q_condition, neighbor_list, thread_num)
        self.assertEqual(expected, actual)
