# -*- coding: utf-8 -*-

from .context import op_tools

import unittest

import numpy as np


def f1(j, voronoi_area_list, distance_list):
    weight = voronoi_area_list[j] / np.sum(voronoi_area_list)
    return weight


def f2(j, voronoi_area_list, distance_list):
    weight = 1.0 / float(len(distance_list))
    return weight


def f3(j, voronoi_area_list, distance_list):
    sum_dist = 0
    for i in range(len(distance_list)):
        sum_dist += 1.0/distance_list[i]
    weight = (1.0/distance_list[j]) / np.sum(sum_dist)
    return weight


class TestOp_py(unittest.TestCase):

    def test_spherical_order_parameter(self):
        coord = [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0]]
        neighbor_list = [[1, 2], [0, 2], [0, 1]]
        nei_area = [[1, 1], [1, 1], [1, 1]]
        box_length = [5 for i in range(3)]
        q_condition = {'ave_times': 1, 'oi_oj': [0], 'o_factor': [
            0], 'b_in_Q': 1, 'l_in_Q': [4], 'p_in_Q': [0], 'function_in_Q2' : [f1]}
        thread_num = 1

        expected = {'l=4_f1=f1_a=0_b=0': [0.82915619758885, 0.54486236794258, 0.54486236794258],
                    'l=4_f1=f1_a=0_b=1': [0.48591265790378, 0.48591265790378, 0.48591265790378],
                    'l=4_f1=f1_a=1_b=0': [0.63962697782467, 0.63962697782467, 0.63962697782467],
                    'l=4_f1=f1_a=1_b=1': [0.48591265790378, 0.48591265790378, 0.48591265790378]}

        actual = op_tools.op_qw2_spherical.spherical_order_parameter(
            coord, box_length, q_condition, neighbor_list, nei_area, thread_num)
        print(actual)
        self.assertEqual(expected, actual)


        # bcc crystal structure
        coord = [
            [0.5, 0.5, 0.5], [0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0],
            [1, 1, 0], [0.0, 0.0, 1.0], [1.0, 0.0, 1.0], [0.0, 1.0, 1.0], [1, 1, 1]]
        neighbor_list = [[1, 2, 3, 4, 5, 6, 7, 8], [
            0], [1], [2], [3], [4], [5], [6], [7]]
        nei_area = [[1, 1, 1, 1, 1, 1, 1, 1], [
            1], [1], [1], [1], [1], [1], [1], [1]]

        box_length = [5 for i in range(3)]
        q_condition = {'ave_times': 0, 'oi_oj': [0], 'o_factor': [
            0], 'b_in_Q': 0, 'l_in_Q': [4, 6], 'p_in_Q': [0], 'function_in_Q2': [f2]}
        thread_num = 1

        expected = {
            'l=4_f1=f2_a=0_b=0': [0.50917507721732, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
            'l=6_f1=f2_a=0_b=0': [0.62853936105471, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]}

        actual = op_tools.op_qw2_spherical.spherical_order_parameter(
            coord, box_length, q_condition, neighbor_list, nei_area, thread_num)
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
        nei_area = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1], [1], [1], [1], [1], [1], [1], [1], [1], [1], [1], [1], [1]]

        box_length = [5 for i in range(3)]
        q_condition = {'ave_times': 0, 'oi_oj': [0], 'o_factor': [
            0], 'b_in_Q': 0, 'l_in_Q': [4, 6], 'function_in_Q2': [f1, f2, f3]}
        thread_num = 1

        expected = {'l=4_f1=f1_a=0_b=0': [0.09722222222222, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
                    'l=4_f1=f2_a=0_b=0': [0.09722222222222, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
                    'l=4_f1=f3_a=0_b=0': [0.09722222222222, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
                    'l=6_f1=f1_a=0_b=0': [0.48476168522368, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
                    'l=6_f1=f2_a=0_b=0': [0.48476168522368, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
                    'l=6_f1=f3_a=0_b=0': [0.48476168522368, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]}

        actual = op_tools.op_qw2_spherical.spherical_order_parameter(
            coord, box_length, q_condition, neighbor_list, nei_area, thread_num)
        self.assertEqual(expected, actual)
