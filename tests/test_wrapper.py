# -*- coding: utf-8 -*-
from .context import op_tools

import unittest


class TestOrderParam(unittest.TestCase):

    def test_op_analyze(self):
        coord = [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0]]
        direct = [[1, 0, 0], [1, 0, 0]]
        box_length = [2.0, 2.0, 2.0]
        NR_name = 'N1'
        n_list = [[1], [0]]
        nei_area = []
        op_settings = {'ave_times': 0, 'neighbor': [1], 'n_in_S': [2],  'analysis_type': ['S']}
        op_datas = {}
        thread_num = 1

        expected = {'S_N1_a=0_n=2': [1.0, 1.0]}
        actual = op_tools.wrapper.op_analyze_with_neighbor_list(
            coord, direct, box_length, NR_name, op_settings, n_list, nei_area, op_datas, thread_num)
        self.assertEqual(expected, actual)

        NR_name = 'N2'
        expected = {'S_N1_a=0_n=2': [1.0, 1.0],  'S_N2_a=0_n=2': [1.0, 1.0]}
        actual = op_tools.wrapper.op_analyze_with_neighbor_list(
            coord, direct, box_length, NR_name, op_settings, n_list, nei_area, op_datas, thread_num)
        self.assertEqual(expected, actual)

    def test_op_analyze2(self):
        coord = [[0.0, 0.0, 0.0], [0.5, 0.0, 0.0]]
        direct = [[1, 0, 0], [1, 0, 0]]
        box_length = [2.0, 2.0, 2.0]
        op_settings = {'ave_times': 0, 'neighbor': [
            1], 'radius': [], 'n_in_S': [2], 'analysis_type': ['S']}
        thread_num = 1

        expected = {'S_N1_a=0_n=2':  [1.0, 1.0]}
        actual = op_tools.wrapper.op_analyze(
            coord, direct, box_length, op_settings, thread_num)
        self.assertEqual(expected, actual)

    def test_op_analyze_delaunay(self):
        coord = [[0.0, 0.0, 0.0], [0.5, 0.0, 0.0]]
        direct = [[1, 0, 0], [1, 0, 0]]
        box_length = [2.0, 2.0, 2.0]
        op_settings = {'ave_times': 0, 'Delaunay': ['standard'], 'n_in_S': [2], 'analysis_type': ['S']}
        thread_num = 1

        expected = {'S_Delaunay_a=0_n=2':  [1.0, 1.0]}
        actual = op_tools.wrapper.op_analyze(
            coord, direct, box_length, op_settings, thread_num)
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
