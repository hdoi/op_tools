# -*- coding: utf-8 -*-

from .context import op_tools

import unittest


class TestOp_py(unittest.TestCase):

    def test_w_order_parameter(self):
        coord = [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0]]
        neighbor_list = [[1, 2], [0, 2], [0, 1]]
        direct = [[1, 0, 0], [1, 0.01, 0], [1, 0, 0.1]]
        box_length = [5 for i in range(3)]
        q_condition = {'ave_times': 1, 'b_in_Q': 1, 'l_in_Q': [4]}
        thread_num = 1

        expected = {'l=4_a=0_b=0': [0.12497095917262, 0.04371722396515, 0.04371722396515],
                    'l=4_a=0_b=1': [0.12208942391243, 0.12208942391243, 0.12208942391243],
                    'l=4_a=1_b=0': [0.07080180236764, 0.07080180236764, 0.07080180236764],
                    'l=4_a=1_b=1': [0.12208942391243, 0.12208942391243, 0.12208942391243]}

        actual = op_tools.op_qw_spherical.w_order_parameter(
            coord, direct, box_length, q_condition, neighbor_list, thread_num)
        self.assertEqual(expected, actual)

        # bcc crystal structure
        coord = [
            [0.5, 0.5, 0.5],
            [0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [1, 1, 0],
            [0.0, 0.0, 1.0], [1.0, 0.0, 1.0], [0.0, 1.0, 1.0], [1, 1, 1],
            [1.5, 0.5, 0.5], [0.5, 1.5, 0.5], [0.5, 0.5, 1.5],
            [-0.5, 0.5, 0.5], [0.5, -0.5, 0.5], [0.5, 0.5, -0.5]]
        neighbor_list = [[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
                         [0], [1], [2], [3], [4], [5], [6], [7],
                         [8], [9], [10], [11], [12], [13]]

        direct = [[1, 0, 0] for i in range(15)]
        box_length = [5 for i in range(3)]
        q_condition = {'ave_times': 0, 'b_in_Q': 0, 'l_in_Q': [4, 6]}
        thread_num = 1

        # value in DOI:10.1103/PhysRevB.28.784
        expected = {'l=4_a=0_b=0': [0.15931737313308, 0.0159113779906, 0.1340970468803, 0.19171687171168,
                                    0.1340970468803, 0.0159113779906, 0.1340970468803, 0.19171687171168, 0.1340970468803, 0.0159113779906,
                                    0.19171687171168, 0.1340970468803, -0.00198613790138, 0.19171687171168, 0.1340970468803],
                    'l=6_a=0_b=0': [0.01316060073065, -0.03324579367116, -0.09305950021129, 0.1352384460468,
                                    -0.09305950021129, -0.03324579367116, -0.09305950021129, 0.1352384460468, -0.09305950021129,
                                    -0.03324579367116, 0.1352384460468, -0.09305950021129, -0.01426506282808, 0.1352384460468, -0.09305950021129]}

        actual = op_tools.op_qw_spherical.w_order_parameter(
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

        expected = {'l=4_a=0_b=0': [-0.15931737313308, 0.1340970468803, 0.19171687171168, 0.1340970468803, 0.19171687171168, -0.12223581660314, 0.1340970468803, 0.19171687171168, 0.1340970468803, -0.12223581660314, 0.19171687171168, 0.1340970468803, 0.19171687171168],
                    'l=6_a=0_b=0': [-0.01316060073065, -0.09305950021129, 0.1352384460468, -0.09305950021129, 0.1352384460468, -0.03252118565248, -0.09305950021129, 0.1352384460468, -0.09305950021129, -0.03252118565248, 0.1352384460468, -0.09305950021129, 0.1352384460468]}

        actual = op_tools.op_qw_spherical.w_order_parameter(
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
            'l=4_a=0_b=0': [0.1340970468803, 0.1340970468803, -0.05644123750528, 0.1340970468803, -0.05644123750528, -0.05644123750528, 0.1340970468803, -0.10416723195191, -0.05644123750528, 0.1340970468803, -0.08722950438235, -0.05644123750528, 0.1340970468803],
            'l=6_a=0_b=0': [-0.01244195946489, -0.09305950021129, -0.10567314065894, -0.09305950021129, -0.10567314065894, -0.10567314065894, -0.09305950021129, 0.08802699617305, -0.10567314065894, -0.09305950021129, 0.078126841521, -0.10567314065894, -0.09305950021129]}

        actual = op_tools.op_qw_spherical.w_order_parameter(
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

        expected = {
            'l=4_a=0_b=0': [0.0, 0.0, 0.0],
            'l=6_a=0_b=0': [0.0, 0.0, 0.0]}

        actual = op_tools.op_qw_spherical.w_order_parameter(
            coord, direct, box_length, q_condition, neighbor_list, thread_num)
        self.assertEqual(expected, actual)