# -*- coding: utf-8 -*-

from .context import op_tools

import unittest


class TestOp_py(unittest.TestCase):

    def test_spherical_order_parameter(self):
        coord = [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0]]
        neighbor_list = [[1, 2], [0, 2], [0, 1]]
        direct = [[1, 0, 0], [1, 0.01, 0], [1, 0, 0.1]]
        box_length = [5 for i in range(3)]
        q_condition = {'ave_times': 1, 'b_in_Q': 1, 'l_in_Q': [4]}
        thread_num = 1

        expected = {
            'l=4_a=0_b=0': [0.82915619758885, 0.54486236794258, 0.54486236794258],
            'l=4_a=0_b=1': [0.48591265790378, 0.48591265790378, 0.48591265790378],
            'l=4_a=1_b=0': [0.63962697782467, 0.63962697782467, 0.63962697782467],
            'l=4_a=1_b=1': [0.48591265790378, 0.48591265790378, 0.48591265790378]}

        actual = op_tools.op_qw_spherical.spherical_order_parameter(
            coord, direct, box_length, q_condition, neighbor_list, thread_num)
        self.assertEqual(expected, actual)

        # bcc crystal structure
        coord = [
            [0.5, 0.5, 0.5], [0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0],
            [1, 1, 0], [0.0, 0.0, 1.0], [1.0, 0.0, 1.0], [0.0, 1.0, 1.0], [1, 1, 1]]
        neighbor_list = [[1, 2, 3, 4, 5, 6, 7, 8], [
            0], [1], [2], [3], [4], [5], [6], [7]]

        direct = [[1, 0, 0] for i in range(9)]
        box_length = [5 for i in range(3)]
        q_condition = {'ave_times': 0, 'b_in_Q': 0, 'l_in_Q': [4, 6]}
        thread_num = 1

        # value in DOI:10.1063/1.4774084 .
        expected = {
            'l=4_a=0_b=0': [0.50917507721732, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
            'l=6_a=0_b=0': [0.62853936105471, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]}

        actual = op_tools.op_qw_spherical.spherical_order_parameter(
            coord, direct, box_length, q_condition, neighbor_list, thread_num)
        self.assertEqual(expected, actual)

        # fcc crystal structure
        coord = [
            [0.0, 0.0, 0.0],
            [0.0, 1.0, 1.0], [1.0, 0.0, 1.0], [
                -1.0, 0.0, 1.0], [0.0, -1.0, 1.0],
            [1.0, 1.0, 0.0], [-1.0, 1.0, 0.0], [
                1.0, -1.0, 0.0], [-1.0, -1.0, 0.0],
            [0.0, 1.0, -1.0], [1.0, 0.0, -1.0], [-1.0, 0.0, -1.0], [0.0, -1.0, -1.0]]
        neighbor_list = [[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], [
            0], [1], [2], [3], [4], [5], [6], [7], [8], [9], [10], [11], [12]]

        direct = [[1, 0, 0] for i in range(13)]
        box_length = [5 for i in range(3)]
        q_condition = {'ave_times': 0, 'b_in_Q': 0, 'l_in_Q': [4, 6]}
        thread_num = 1

        expected = {
            'l=4_a=0_b=0': [0.19094065395649, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
            'l=6_a=0_b=0': [0.57452425971407, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]}

        actual = op_tools.op_qw_spherical.spherical_order_parameter(
            coord, direct, box_length, q_condition, neighbor_list, thread_num)
        self.assertEqual(expected, actual)

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

        direct = [[1, 0, 0] for i in range(13)]
        box_length = [5 for i in range(3)]
        q_condition = {'ave_times': 0, 'b_in_Q': 0, 'l_in_Q': [4, 6]}
        thread_num = 1

        expected = {
            'l=4_a=0_b=0': [0.09722222222222, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
            'l=6_a=0_b=0': [0.48476168522368, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]}

        actual = op_tools.op_qw_spherical.spherical_order_parameter(
            coord, direct, box_length, q_condition, neighbor_list, thread_num)
        self.assertEqual(expected, actual)

        # check 0 neighbor
        coord = [
            [0.0, 0.0, 0.0],
            [1.0, 0.0, 0.0],
            [0.5, 3**0.5 / 2.0, 0.0]]
        neighbor_list = [[], [], []]
        direct = [[1, 0, 0] for i in range(3)]
        box_length = [5 for i in range(3)]
        q_condition = {'ave_times': 0, 'b_in_Q': 0, 'l_in_Q': [4, 6]}
        thread_num = 1

        expected = {'l=4_a=0_b=0': [0.0, 0.0, 0.0],
                    'l=6_a=0_b=0': [0.0, 0.0, 0.0]}

        actual = op_tools.op_qw_spherical.spherical_order_parameter(
            coord, direct, box_length, q_condition, neighbor_list, thread_num)
        self.assertEqual(expected, actual)
