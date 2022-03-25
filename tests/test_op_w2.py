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
            0], 'b_in_Q': 1, 'l_in_Q': [4], 'p_in_Q': [0], 'function_in_Q2': [f1]}
        thread_num = 1

        expected = {'l=4_f1=f1_a=0_b=0': [0.12497095917262, 0.04371722396515, 0.04371722396515],
                    'l=4_f1=f1_a=0_b=1': [0.12208942391243, 0.12208942391243, 0.12208942391243],
                    'l=4_f1=f1_a=1_b=0': [0.07080180236764, 0.07080180236764, 0.07080180236764],
                    'l=4_f1=f1_a=1_b=1': [0.12208942391243, 0.12208942391243, 0.12208942391243]}

        actual = op_tools.op_qw2_spherical.w_order_parameter(
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

        expected = {'l=4_f1=f1_a=0_b=0': [0.1340970468803, 0.1340970468803, -0.05644123750528, 0.1340970468803, -0.05644123750528, -0.05644123750528, 0.1340970468803, -0.10416723195191, -0.05644123750528, 0.1340970468803, -0.08722950438235, -0.05644123750528, 0.1340970468803],
                    'l=4_f1=f2_a=0_b=0': [0.1340970468803, 0.1340970468803, -0.05644123750528, 0.1340970468803, -0.05644123750528, -0.05644123750528, 0.1340970468803, -0.10416723195191, -0.05644123750528, 0.1340970468803, -0.08722950438235, -0.05644123750528, 0.1340970468803],
                    'l=4_f1=f3_a=0_b=0': [0.1340970468803, 0.1340970468803, -0.05644123750528, 0.1340970468803, -0.05644123750528, -0.05644123750528, 0.1340970468803, -0.10416723195191, -0.05644123750528, 0.1340970468803, -0.08722950438235, -0.05644123750528, 0.1340970468803],
                    'l=6_f1=f1_a=0_b=0': [-0.01244195946489, -0.09305950021129, -0.10567314065894, -0.09305950021129, -0.10567314065894, -0.10567314065894, -0.09305950021129, 0.08802699617305, -0.10567314065894, -0.09305950021129, 0.078126841521, -0.10567314065894, -0.09305950021129],
                    'l=6_f1=f2_a=0_b=0': [-0.01244195946489, -0.09305950021129, -0.10567314065894, -0.09305950021129, -0.10567314065894, -0.10567314065894, -0.09305950021129, 0.08802699617305, -0.10567314065894, -0.09305950021129, 0.078126841521, -0.10567314065894, -0.09305950021129],
                    'l=6_f1=f3_a=0_b=0': [-0.01244195946489, -0.09305950021129, -0.10567314065894, -0.09305950021129, -0.10567314065894, -0.10567314065894, -0.09305950021129, 0.08802699617305, -0.10567314065894, -0.09305950021129, 0.078126841521, -0.10567314065894, -0.09305950021129]}

        actual = op_tools.op_qw2_spherical.w_order_parameter(
            coord, box_length, q_condition, neighbor_list, nei_area, thread_num)
        self.assertEqual(expected, actual)
