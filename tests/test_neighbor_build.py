# -*- coding: utf-8 -*-

from .context import op_tools

import unittest


class TestNeighborBuild(unittest.TestCase):

    """ test method of neighbor build """
    def test_build_cell(self):
        coord = [[0, 0, 0], [1, 1, 1]]
        box_length = [2, 2, 2]
        thresh_dist = 1.0

        e_cell_list = [[[[0], []], [[], []]], [[[], []], [[], [1]]]]
        e_cell_length = [1.0, 1.0, 1.0]
        e_cell_size = [2, 2, 2]
        expected = [e_cell_list, e_cell_length, e_cell_size]
        actual = op_tools.neighbor_build.build_cell(
            coord, box_length, thresh_dist)
        self.assertEqual((expected == actual), True)

    def test_build_cell(self):
        coord = [[0, 0, 0], [3, 3, 3]]
        box_length = [2, 2, 2]
        thresh_dist = 1.0

        e_cell_list = [[[[0], []], [[], []]], [[[], []], [[], [1]]]]
        e_cell_length = [1.0, 1.0, 1.0]
        e_cell_size = [2, 2, 2]
        expected = [e_cell_list, e_cell_length, e_cell_size]
        actual = op_tools.neighbor_build.build_cell(
            coord, box_length, thresh_dist)
        self.assertEqual((expected == actual), True)

    def test_calc_thresh(self):
        box_length = [10, 10, 10]
        part_num = 300
        target_num = 6
        safe_factor = 1.2

        expected = safe_factor * 1.6838903009606296
        actual = op_tools.neighbor_build.calc_thresh(
            box_length, part_num, target_num, safe_factor)
        self.assertEqual((expected == actual), True)

    def test_build_neighbor_list(self):
        coord = [[0, 0, 0], [0.5, 0, 0]]
        box_length = [2, 2, 2]
        condition = {'mode': 'thresh', 'dist': 1.0}
        thread_num = 1

        expected = [[[1], [0]], [[0.5], [0.5]]]
        actual = op_tools.neighbor_build.build_neighbor_list(
            coord, box_length, condition, thread_num)
        self.assertEqual((expected == actual), True)

        condition = {'mode': 'thresh', 'dist': 1.2}

        expected = [[[1], [0]], [[0.5], [0.5]]]
        actual = op_tools.neighbor_build.build_neighbor_list(
            coord, box_length, condition, thread_num)
        self.assertEqual((expected == actual), True)

    def test_build_neighbor_list_N(self):
        coord = [[0, 0, 0], [0.5, 0, 0]]
        box_length = [8, 8, 8]
        condition = {'mode': 'neighbor', 'dist': 1.0, 'num': 1}
        thread_num = 1

        expected = [[[1], [0]], [[0.5], [0.5]]]
        actual = op_tools.neighbor_build.build_neighbor_list(
            coord, box_length, condition, thread_num)
        self.assertEqual((expected == actual), True)

    def test_build_neighbor_wrapper(self):
        coord = [[0, 0, 0], [0.5, 0, 0]]
        box_length = [8, 8, 8]
        op_settings = {'neighbor': [1]}
        thread_num = 1

        expected = {'N1': [[[1], [0]], [[0.5], [0.5]]]}
        actual = op_tools.neighbor_build.build_neighbor_wrapper(
            coord, box_length, op_settings, thread_num)
        self.assertEqual((expected == actual), True)

    def test_delaunay_neighbor(self):
        import random

        random.seed(10)
        box_length = [10, 10, 10]

        coord = []
        i_ijk = [[i, j, k] for i in range(4)
                 for j in range(4) for k in range(4)]
        for ijk in i_ijk:
            xyz = [0, 0, 0]
            for i1 in range(3):
                xyz[i1] = 3.2*ijk[i1] + random.normalvariate(0, 0.3)
            coord.append(xyz)
        op_settings = {'Delaunay': ['standard']}
        thread_num = 1

        expected = {'Delaunay': [[[63, 48, 15, 12, 3, 13, 16, 19, 1, 52, 4, 7],
                                  [49, 61, 13, 5, 15, 53, 0, 29, 2,
                                      17, 52, 21, 16, 54, 18, 32, 20],
                                  [14, 62, 50, 54, 30, 3, 18, 49,
                                      51, 48, 1, 61, 19, 55, 17, 21],
                                  [12, 63, 60, 51, 0, 48, 15, 56, 19, 62,
                                   31, 16, 14, 2, 11, 30, 58, 24, 27, 26],
                                  [7, 55, 52, 11, 8, 59, 48, 0, 20, 16],
                                  [53, 52, 1, 57, 49, 21, 6, 54,
                                      9, 37, 10, 11, 50, 20],
                                  [54, 10, 55, 5, 7, 53, 22, 21,
                                      57, 26, 23, 37, 38, 27],
                                  [4, 55, 11, 8, 59, 54, 6, 20, 48,
                                      23, 0, 27, 10, 58, 16, 19],
                                  [56, 59, 11, 7, 4, 52, 9, 40, 57, 41],
                                  [57, 25, 61, 13, 11, 8, 56, 53, 10,
                                      5, 58, 24, 26, 14, 29, 21, 31],
                                  [58, 6, 59, 57, 14, 26, 9, 11, 42,
                                      50, 55, 7, 5, 27, 25, 21, 38, 37],
                                  [8, 56, 59, 24, 27, 7, 4, 9, 52, 3, 58, 12,
                                   57, 10, 15, 13, 20, 53, 31, 5, 26, 21],
                                  [63, 0, 15, 60, 3, 56, 16, 31, 11],
                                  [61, 1, 49, 15, 0, 60, 9, 29, 16, 56,
                                      31, 45, 44, 11, 32, 25, 41, 24],
                                  [62, 2, 50, 58, 3, 30, 61, 10,
                                      49, 18, 26, 9, 57, 17, 25],
                                  [0, 12, 63, 48, 60, 51, 3, 13, 1,
                                      49, 56, 16, 31, 44, 32, 52, 11],
                                  [31, 19, 28, 23, 3, 0, 20, 29, 12,
                                      15, 48, 13, 1, 33, 7, 4, 21, 52],
                                  [29, 33, 18, 45, 25, 30, 21, 1,
                                      46, 34, 61, 22, 26, 37, 2, 14],
                                  [30, 22, 17, 34, 2, 38, 14,
                                      21, 54, 33, 23, 1, 37, 35],
                                  [31, 16, 28, 3, 30, 0, 23, 48, 24, 2, 26, 7, 54],
                                  [23, 39, 27, 16, 24, 7, 4, 21, 43,
                                      52, 11, 29, 5, 37, 33, 41, 1],
                                  [22, 5, 37, 25, 29, 17, 20, 18, 38, 6, 54, 1, 33,
                                   9, 26, 57, 24, 52, 16, 41, 39, 2, 10, 11],
                                  [38, 18, 21, 30, 37, 23, 6,
                                      54, 26, 34, 17, 33, 27],
                                  [20, 39, 16, 27, 19, 28, 22, 7,
                                      38, 30, 18, 35, 32, 6, 54, 33],
                                  [27, 11, 20, 43, 40, 25, 31, 28,
                                      19, 26, 9, 3, 41, 21, 13],
                                  [9, 26, 17, 29, 21, 24, 41, 42, 45, 61,
                                   13, 10, 40, 46, 28, 31, 37, 14, 38],
                                  [25, 42, 58, 10, 30, 27, 24, 22, 14, 17, 34,
                                   46, 9, 38, 21, 6, 19, 11, 28, 43, 3],
                                  [24, 11, 20, 23, 43, 26, 7, 39,
                                      28, 58, 3, 10, 22, 42, 38, 6],
                                  [31, 19, 16, 47, 35, 32, 30, 29, 23, 44, 24,
                                   27, 33, 45, 39, 34, 43, 40, 25, 26, 41, 42],
                                  [17, 33, 16, 45, 25, 28, 31,
                                      13, 1, 21, 61, 9, 20],
                                  [18, 19, 2, 22, 28, 34, 14,
                                      26, 17, 46, 3, 23, 54, 35],
                                  [19, 28, 16, 3, 12, 15, 29, 24, 13, 11, 25, 9],
                                  [47, 35, 44, 51, 28, 48, 36, 39, 45,
                                      15, 33, 23, 13, 52, 55, 49, 1],
                                  [45, 17, 29, 46, 37, 34, 44, 32, 47, 49, 28,
                                   18, 16, 21, 50, 36, 22, 39, 53, 20, 23, 52],
                                  [46, 50, 18, 42, 35, 30, 33, 62,
                                      44, 17, 38, 22, 26, 37, 28],
                                  [47, 32, 44, 51, 28, 34, 36, 39, 62,
                                      50, 43, 23, 30, 42, 18, 55, 38, 54],
                                  [39, 43, 52, 40, 55, 32, 35,
                                      38, 41, 37, 59, 53, 33],
                                  [38, 33, 21, 53, 41, 22, 5, 36, 39, 42, 34, 57,
                                   46, 17, 49, 52, 18, 54, 6, 20, 25, 50, 10],
                                  [22, 37, 42, 39, 18, 21, 23, 36, 34, 26,
                                   43, 54, 35, 6, 27, 55, 10, 25, 50, 59],
                                  [36, 23, 20, 43, 40, 38, 32,
                                      35, 27, 41, 37, 28, 33, 21],
                                  [43, 41, 59, 36, 39, 44, 56,
                                      8, 24, 52, 45, 28, 25],
                                  [40, 43, 57, 45, 37, 25, 42, 36, 44, 8, 39,
                                   56, 53, 46, 24, 52, 61, 21, 13, 20, 28],
                                  [46, 34, 26, 38, 43, 58, 10, 41, 50, 25,
                                   59, 62, 37, 57, 35, 44, 27, 28, 55],
                                  [40, 39, 36, 41, 59, 27, 24,
                                      44, 42, 20, 35, 38, 28, 26],
                                  [47, 32, 35, 51, 60, 40, 45, 15, 28, 43,
                                   33, 56, 59, 34, 13, 41, 62, 61, 42],
                                  [33, 46, 17, 29, 44, 41, 32, 61,
                                      49, 13, 50, 28, 25, 40, 57],
                                  [34, 50, 42, 45, 33, 62, 17,
                                      30, 26, 61, 41, 37, 25, 57],
                                  [32, 35, 44, 28, 33],
                                  [63, 0, 51, 15, 60, 3, 32, 19,
                                      52, 16, 55, 4, 2, 7, 54],
                                  [1, 61, 13, 5, 15, 53, 50, 2,
                                      14, 45, 33, 52, 54, 37, 32],
                                  [62, 14, 2, 46, 34, 49, 61, 58, 51, 54,
                                   10, 35, 45, 42, 33, 57, 5, 37, 55, 38],
                                  [60, 48, 63, 3, 15, 44, 32,
                                      56, 62, 35, 2, 50, 59, 55],
                                  [4, 55, 53, 5, 36, 8, 11, 48, 0, 59, 15, 1,
                                   57, 49, 20, 40, 32, 37, 41, 21, 16, 33],
                                  [5, 52, 57, 1, 49, 6, 37, 54, 9, 41, 36, 11, 33],
                                  [6, 2, 55, 7, 5, 53, 50, 22, 18, 21,
                                      30, 49, 1, 48, 38, 37, 23, 19, 35],
                                  [4, 7, 52, 54, 6, 59, 36, 48, 51,
                                      10, 2, 32, 35, 38, 50, 42],
                                  [8, 59, 11, 60, 3, 12, 51, 15, 58,
                                      40, 9, 44, 13, 57, 62, 41, 61],
                                  [9, 53, 5, 41, 10, 8, 61, 11, 56, 52,
                                      6, 37, 42, 21, 14, 50, 45, 46],
                                  [10, 59, 14, 62, 56, 26, 11,
                                      50, 42, 9, 3, 7, 27],
                                  [8, 56, 11, 58, 40, 7, 4, 55, 43, 10,
                                      60, 52, 51, 44, 36, 62, 42, 38],
                                  [51, 12, 63, 48, 3, 15, 56, 13, 44, 62, 59],
                                  [49, 13, 1, 9, 50, 14, 45, 2, 57,
                                      29, 17, 56, 46, 44, 25, 41],
                                  [14, 50, 2, 51, 3, 58, 60, 46,
                                      34, 56, 35, 59, 44, 42],
                                  [12, 0, 48, 15, 60, 51, 3]],
                                 [[0.33179, 0.43499, 0.45422, 0.49542, 1.04666, 2.19058, 2.90677, 2.93063, 3.04985, 3.29121, 3.44495, 3.59979],
                                  [0.35233, 1.06129, 1.24141, 2.73629, 2.75229, 2.86511, 3.04985, 3.34812, 3.3545,
                                   3.60518, 3.72011, 4.14693, 4.17159, 4.20859, 4.47965, 4.79462, 5.27511],
                                  [1.07722, 1.30251, 1.48718, 2.64295, 2.87279, 3.08455, 3.1677, 3.18724,
                                     3.20248, 3.3518, 3.3545, 3.43029, 4.15359, 4.18034, 4.47763, 4.99964],
                                  [0.64675, 0.79415, 0.84695, 1.03546, 1.04666, 1.07948, 1.19992, 2.53649, 2.659, 2.76045,
                                     2.80857, 2.8912, 3.04997, 3.08455, 3.27946, 3.75328, 3.84742, 4.21789, 4.4114, 4.90799],
                                  [0.32616, 0.71476, 1.07854, 2.72503, 2.75342,
                                     2.93697, 3.32231, 3.44495, 3.47859, 4.4669],
                                  [0.41657, 2.733, 2.73629, 2.81358, 2.90249, 3.07318, 3.09633,
                                     3.17129, 3.53037, 3.65641, 4.187, 4.48226, 4.69406, 4.80481],
                                  [0.35605, 2.77422, 2.88071, 3.09633, 3.10311, 3.37629, 3.57369,
                                     3.96328, 4.18242, 4.49137, 4.61257, 4.64371, 4.67277, 4.97599],
                                  [0.32616, 0.7699, 2.59717, 2.68073, 2.86519, 3.08754, 3.10311, 3.33269,
                                     3.47414, 3.49019, 3.59979, 3.62335, 3.90934, 3.94492, 4.46436, 4.68327],
                                  [0.75653, 0.86767, 0.89257, 2.68073, 2.75342,
                                     3.07682, 3.20731, 3.25919, 3.40746, 4.07189],
                                  [1.25536, 2.77933, 2.83544, 3.05159, 3.07541, 3.20731, 3.35557, 3.46107, 3.51735,
                                     3.53037, 3.83133, 4.04025, 4.15041, 4.20187, 4.27639, 4.30533, 5.10664],
                                  [0.59711, 2.77422, 3.05429, 3.13896, 3.2257, 3.28079, 3.51735, 3.64184, 3.68801,
                                     3.68822, 3.87994, 3.90934, 4.187, 4.48287, 4.53038, 5.02299, 5.07677, 5.26531],
                                  [0.89257, 1.32427, 1.66921, 2.4006, 2.47426, 2.59717, 2.72503, 3.07541, 3.16991, 3.27946, 3.29252,
                                     3.51225, 3.51475, 3.64184, 3.72556, 4.13881, 4.1498, 4.28694, 4.33225, 4.48226, 4.56238, 5.19586],
                                  [0.30293, 0.49542, 0.57263, 0.62229, 0.64675,
                                     2.69257, 2.98451, 3.01638, 3.51225],
                                  [0.9891, 1.24141, 1.31365, 1.7973, 2.19058, 2.65066, 3.05159, 3.32431, 3.58371,
                                     3.61907, 3.80164, 3.80398, 3.96641, 4.13881, 4.28723, 4.37, 4.90654, 5.0601],
                                  [0.65837, 1.07722, 1.11615, 2.80239, 3.04997, 3.17736, 3.2133, 3.2257,
                                     3.24833, 3.62543, 4.00348, 4.20187, 4.47088, 4.57831, 4.99684],
                                  [0.45422, 0.57263, 0.62148, 0.7991, 1.00354, 1.16553, 1.19992, 1.7973, 2.75229,
                                     2.90382, 2.9329, 3.00708, 3.12642, 3.22341, 3.43804, 3.50423, 3.72556],
                                  [0.6247, 0.74594, 0.88741, 2.76273, 2.8912, 2.90677, 2.9242, 2.93026, 2.98451,
                                     3.00708, 3.2141, 3.58371, 4.17159, 4.20682, 4.46436, 4.4669, 4.64708, 4.67],
                                  [0.5334, 2.51485, 2.75181, 2.90701, 3.03717, 3.34672, 3.55718, 3.60518,
                                     3.64814, 3.76112, 3.77995, 4.0291, 4.10676, 4.35043, 4.47763, 4.57831],
                                  [0.96482, 2.25243, 2.75181, 2.96597, 3.1677, 3.55613, 3.62543,
                                     3.67505, 3.9647, 4.04328, 4.11338, 4.47965, 4.50485, 4.53747],
                                  [0.41029, 0.74594, 0.80515, 2.659, 2.69023, 2.93063, 3.06542,
                                     3.18304, 3.76002, 4.15359, 4.51535, 4.68327, 5.14957],
                                  [0.52102, 2.47404, 2.80572, 2.9242, 3.04969, 3.33269, 3.47859, 3.64011, 3.93389,
                                     4.01342, 4.1498, 4.43874, 4.80481, 4.85311, 4.91728, 5.12144, 5.27511],
                                  [2.66274, 3.07318, 3.34313, 3.47477, 3.50503, 3.55718, 3.64011, 3.67505, 3.74928, 3.96328, 4.10719, 4.14693,
                                     4.27103, 4.30533, 4.31463, 4.47035, 4.62612, 4.63276, 4.64708, 4.72137, 4.84018, 4.99964, 5.02299, 5.19586],
                                  [1.89018, 2.25243, 2.66274, 2.98919, 3.44451, 3.44452, 3.57369,
                                     3.66382, 3.9613, 4.01239, 4.0291, 4.55576, 4.67928],
                                  [0.52102, 2.34791, 2.76273, 3.05218, 3.06542, 3.18583, 3.44452, 3.49019,
                                     3.79281, 3.99515, 4.11338, 4.15469, 4.1583, 4.61257, 4.62637, 4.99409],
                                  [0.41606, 2.4006, 3.04969, 3.11116, 3.50907, 3.54174, 3.56257, 3.61765,
                                     3.76002, 3.77311, 4.04025, 4.21789, 4.44811, 4.62612, 5.0601],
                                  [2.77933, 2.80401, 3.03717, 3.1183, 3.47477, 3.54174, 3.55771, 4.17683, 4.25846,
                                     4.34073, 4.37, 4.53038, 4.53046, 4.599, 4.617, 4.623, 4.87629, 4.99684, 5.08328],
                                  [2.80401, 3.16319, 3.26438, 3.28079, 3.33691, 3.51676, 3.77311, 3.9613, 4.00348, 4.10676, 4.11832,
                                     4.13489, 4.15041, 4.17593, 4.31463, 4.49137, 4.51535, 4.56238, 4.71715, 4.72679, 4.90799],
                                  [0.41606, 2.47426, 2.80572, 3.05218, 3.08075, 3.51676, 3.62335, 3.80323,
                                     3.88256, 4.27181, 4.4114, 4.48287, 4.67928, 4.70376, 4.80693, 4.97599],
                                  [0.55036, 0.80515, 0.88741, 2.90547, 2.93922, 3.06299, 3.14411, 3.18153, 3.18583, 3.26944, 3.61765,
                                     3.88256, 4.02694, 4.18783, 4.28176, 4.34866, 4.44935, 4.52732, 4.617, 4.71715, 5.29847, 5.4298],
                                  [0.5334, 2.68679, 2.93026, 3.09206, 3.1183, 3.18153, 3.20814,
                                     3.32431, 3.34812, 3.50503, 3.54884, 4.27639, 4.43874],
                                  [0.96482, 2.69023, 2.87279, 2.98919, 3.14411, 3.14555, 3.17736,
                                     3.33691, 3.34672, 3.65593, 3.75328, 3.99515, 4.12393, 4.27315],
                                  [0.41029, 0.55036, 0.6247, 2.80857, 3.01638, 3.12642,
                                     3.20814, 3.56257, 3.80164, 4.33225, 4.623, 5.10664],
                                  [0.29005, 0.47201, 0.88559, 2.73634, 3.06299, 3.12603, 3.23438, 3.35069, 3.38382,
                                     3.43804, 3.48445, 4.1583, 4.28723, 4.34085, 4.36347, 4.74963, 4.79462],
                                  [0.82951, 2.51485, 2.68679, 2.85431, 2.95561, 3.25536, 3.4403, 3.48445, 3.58091, 3.81282, 4.02694,
                                     4.04328, 4.20682, 4.27103, 4.27314, 4.37183, 4.55576, 4.58395, 4.78773, 4.91728, 4.99409, 5.2088],
                                  [0.76592, 2.84647, 2.96597, 3.00498, 3.04709, 3.14555, 3.25536, 3.42058,
                                     3.75504, 3.76112, 3.85138, 4.01239, 4.11832, 4.27079, 4.34866],
                                  [0.31851, 0.47201, 1.01192, 2.87758, 2.93922, 3.04709, 3.45808, 3.4935, 3.9458,
                                     3.9919, 3.99607, 4.15469, 4.27315, 4.51204, 4.53747, 4.56269, 4.60382, 5.47139],
                                  [0.85561, 2.75437, 2.87737, 2.92713, 2.97199, 3.23438, 3.45808,
                                     3.80903, 3.86171, 3.86439, 3.87714, 4.28605, 4.37183],
                                  [2.64733, 2.95561, 3.34313, 3.3944, 3.39786, 3.44451, 3.65641, 3.86439, 4.21013, 4.2269, 4.27079, 4.27901,
                                     4.3248, 4.35043, 4.45038, 4.4834, 4.50485, 4.59136, 4.64371, 4.85311, 4.87629, 4.89295, 5.26531],
                                  [1.89018, 2.64733, 3.25938, 3.3321, 3.55613, 3.74928, 3.79281, 3.80903, 3.85138, 4.17593,
                                     4.31881, 4.58383, 4.60382, 4.67277, 4.80693, 4.86757, 5.07677, 5.08328, 5.08446, 5.43119],
                                  [0.85561, 2.34791, 2.47404, 2.65991, 3.00314, 3.3321, 3.35069,
                                     3.4935, 3.80323, 4.12177, 4.21013, 4.28176, 4.58395, 4.84018],
                                  [0.7235, 2.20038, 2.76638, 2.92713, 3.00314, 3.11145, 3.24526,
                                     3.25919, 3.50907, 4.20453, 4.27602, 4.52732, 4.53046],
                                  [2.20038, 2.82698, 2.96993, 3.37546, 3.39786, 3.55771, 3.74558, 3.86171, 4.03034, 4.07189, 4.12177,
                                     4.13925, 4.23092, 4.31908, 4.44811, 4.5413, 4.59178, 4.72137, 4.90654, 5.12144, 5.29847],
                                  [2.66726, 3.00498, 3.16319, 3.25938, 3.56544, 3.67993, 3.68801, 3.74558, 4.03433,
                                     4.17683, 4.19565, 4.22666, 4.2269, 4.39964, 4.51204, 4.58672, 4.70376, 5.4298, 5.452],
                                  [0.7235, 2.65991, 2.75437, 2.82698, 3.00299, 3.08075, 3.11116,
                                     3.36606, 3.56544, 3.93389, 3.99607, 4.31881, 4.44935, 4.72679],
                                  [0.77784, 0.88559, 1.01192, 2.56795, 2.687, 3.11145, 3.13615, 3.22341, 3.26944, 3.36606,
                                     3.4403, 3.5462, 3.74411, 3.75504, 3.96641, 4.03034, 4.10624, 4.3299, 4.58672],
                                  [0.82951, 2.71042, 2.90701, 3.09206, 3.13615, 3.37546, 3.38382, 3.40254,
                                     3.48415, 3.80398, 3.99806, 4.18783, 4.25846, 4.27602, 4.71178],
                                  [0.76592, 2.59738, 2.66726, 2.71042, 2.85431, 3.23778, 3.64814,
                                     3.65593, 4.13489, 4.27891, 4.31908, 4.3248, 4.599, 5.01982],
                                  [0.29005, 0.31851, 0.77784, 2.90547, 3.58091],
                                  [0.35132, 0.43499, 0.72799, 0.7991, 0.82081, 1.07948, 3.12603, 3.18304,
                                     3.21297, 3.2141, 3.22132, 3.32231, 3.3518, 3.47414, 4.28338],
                                  [0.35233, 0.87247, 1.31365, 2.90249, 2.90382, 3.01948, 3.07115, 3.18724,
                                     3.24833, 3.48415, 3.81282, 3.94074, 4.18013, 4.45038, 4.74963],
                                  [0.8761, 1.11615, 1.48718, 2.59738, 2.84647, 3.07115, 3.11843, 3.3012, 3.37169, 3.59728,
                                     3.68822, 3.9919, 3.99806, 4.03433, 4.27314, 4.5834, 4.69406, 4.89295, 4.91745, 5.08446],
                                  [0.35331, 0.72799, 0.73482, 1.03546, 1.16553, 2.56795, 2.73634,
                                     2.7379, 2.74996, 2.87758, 3.20248, 3.37169, 3.42293, 3.6857],
                                  [1.07854, 1.44285, 2.45339, 2.733, 2.87737, 3.07682, 3.16991, 3.21297, 3.29121, 3.30258, 3.50423,
                                     3.72011, 3.81925, 3.94074, 4.01342, 4.20453, 4.34085, 4.4834, 4.5413, 4.63276, 4.67, 5.2088],
                                  [0.41657, 2.45339, 2.66717, 2.86511, 3.01948, 3.37629, 3.3944,
                                     3.45121, 3.46107, 4.23092, 4.28605, 4.28694, 4.78773],
                                  [0.35605, 2.64295, 2.81338, 3.08754, 3.17129, 3.45121, 3.59728, 3.66382, 3.9647, 4.10719,
                                     4.12393, 4.18013, 4.20859, 4.28338, 4.58383, 4.59136, 4.62637, 5.14957, 5.47139],
                                  [0.71476, 0.7699, 1.44285, 2.81338, 2.88071, 2.9568, 2.97199, 3.22132,
                                     3.6857, 3.87994, 4.18034, 4.36347, 4.56269, 4.86757, 4.91745, 5.452],
                                  [0.75653, 0.97229, 1.32427, 2.45519, 2.53649, 2.69257, 2.7379, 2.9329, 3.035,
                                     3.24526, 3.35557, 3.5462, 3.61907, 3.66926, 3.82787, 4.13925, 4.16428],
                                  [1.25536, 2.66717, 2.81358, 2.96993, 3.13896, 3.40746, 3.49838, 3.51475, 3.66926,
                                     3.81925, 4.18242, 4.27901, 4.39964, 4.47035, 4.47088, 4.5834, 4.71178, 5.01982],
                                  [0.59711, 2.69331, 2.80239, 2.80773, 3.035, 3.26438, 3.29252,
                                     3.3012, 3.67993, 3.83133, 3.84742, 3.94492, 4.27181],
                                  [0.86767, 0.97229, 1.66921, 2.69331, 2.76638, 2.86519, 2.93697, 2.9568, 3.00299,
                                     3.05429, 3.19493, 3.30258, 3.42293, 3.74411, 3.87714, 4.00914, 4.19565, 5.43119],
                                  [0.35331, 0.62229, 0.67055, 0.82081, 0.84695, 1.00354,
                                     2.45519, 2.65066, 2.687, 2.88608, 3.19493],
                                  [0.87247, 0.9891, 1.06129, 2.83544, 3.11843, 3.2133, 3.40254, 3.43029,
                                     3.49838, 3.54884, 3.77995, 4.16428, 4.27891, 4.3299, 4.34073, 4.59178],
                                  [0.65837, 0.8761, 1.30251, 2.74996, 2.76045, 2.80773, 2.88608,
                                     3.23778, 3.42058, 3.82787, 3.9458, 4.00914, 4.10624, 4.22666],
                                  [0.30293, 0.33179, 0.35132, 0.62148, 0.67055, 0.73482, 0.79415]],
                                 [[0.61462, 4.12198, 4.33149, 0.53566, 0.844, 0.09555, 3.26694, 0.45846, 0.39083, 1.95251, 0.7735, 0.16384],
                                  [7.55932, 1.29154, 5.34709, 5.58071, 0.56495, 1.64842, 0.39083, 3.48983, 1.36706,
                                     0.68516, 2.1109, 1.47598, 0.49861, 0.05506, 0.42764, 0.00134, 0.01252],
                                  [5.04136, 2.34394, 4.74771, 9.82351, 4.37255, 1.81166, 2.86898, 2.64279,
                                     0.79359, 1.71483, 1.36706, 0.00128, 0.07699, 0.19609, 0.07727, 0.00021],
                                  [3.05794, 0.74885, 1.99371, 1.18447, 0.844, 1.47306, 0.29275, 3.34815, 4.88664, 2.2375,
                                     1.62732, 0.04197, 1.1848, 1.81166, 1.68113, 1.06015, 0.94801, 0.40097, 0.0112, 0.29244],
                                  [6.75767, 2.58928, 7.56053, 0.56162, 0.52124,
                                     0.11271, 0.53455, 0.7735, 1.20349, 0.0891],
                                  [11.29989, 1.88118, 5.58071, 2.79277, 1.4817, 9.0035, 4.88893,
                                     3.39598, 0.93639, 0.24776, 0.07779, 0.07874, 2e-05, 0.07126],
                                  [12.17242, 10.72408, 1.97368, 4.88893, 2.72498, 0.41325, 4.86441,
                                     2.12892, 0.08402, 1.03784, 0.41825, 0.62449, 0.85468, 0.36573],
                                  [6.75767, 4.83415, 4.26439, 0.59012, 0.75189, 1.27925, 2.72498, 3.6986,
                                     0.58051, 2.75481, 0.16384, 1.88454, 0.68835, 0.10788, 0.09868, 0.06814],
                                  [3.45076, 4.89012, 5.181, 0.59012, 0.52124,
                                     1.86539, 0.69161, 0.62916, 2.24711, 0.31697],
                                  [11.42534, 9.93703, 5.85423, 3.57877, 5.05351, 0.69161, 1.5114, 0.2645, 2.47565,
                                     0.93639, 0.03291, 0.8155, 0.7833, 1.28663, 0.09133, 1.34006, 0.00858],
                                  [12.75248, 10.72408, 1.03503, 7.29315, 0.05675, 4.65033, 2.47565, 0.01716, 4.65273,
                                     0.07242, 0.91765, 0.68835, 0.07779, 0.24242, 0.00067, 0.14672, 0.38121, 0.18548],
                                  [5.181, 4.28642, 0.52253, 6.98258, 4.15064, 4.26439, 0.56162, 5.05351, 1.10301, 1.68113, 2.57198,
                                     0.00089, 0.2587, 0.01716, 0.11212, 0.21353, 0.07422, 0.13993, 0.14031, 0.07874, 0.00236, 0.11168],
                                  [0.44765, 0.53566, 2.97685, 0.96844, 3.05794,
                                     0.32023, 0.02062, 0.00772, 0.00089],
                                  [6.84771, 5.34709, 1.18404, 10.1943, 0.09555, 0.07136, 3.57877, 3.21424, 1.31917,
                                     1.44669, 0.5688, 0.65031, 0.98214, 0.21353, 0.04137, 0.04753, 0.01907, 0.00066],
                                  [4.03485, 5.04136, 3.13, 4.82242, 1.1848, 3.04708, 3.12431, 0.05675,
                                     0.27438, 0.04375, 2.21196, 1.28663, 0.07259, 0.54849, 0.06992],
                                  [4.33149, 2.97685, 0.06565, 1.74455, 2.34654, 0.43611, 0.29275, 10.1943, 0.56495,
                                     0.01905, 0.76746, 1.03713, 0.45561, 0.71321, 0.29277, 0.27907, 0.11212],
                                  [3.00157, 3.9416, 4.40323, 3.99725, 0.04197, 3.26694, 4.28531, 5.97654, 0.02062,
                                     1.03713, 0.001, 1.31917, 0.49861, 0.28145, 0.09868, 0.0891, 0.15599, 0.12391],
                                  [10.4833, 4.78738, 7.88429, 1.84523, 5.42426, 0.7676, 1.88516, 0.68516,
                                     1.83389, 0.2542, 0.77778, 0.08285, 1.24497, 0.00957, 0.07727, 0.54849],
                                  [11.4364, 10.07051, 7.88429, 5.07466, 2.86898, 0.16104, 0.04375,
                                     1.47064, 1.11866, 0.3781, 0.15447, 0.42764, 0.00321, 0.09627],
                                  [3.88892, 3.9416, 4.11413, 4.88664, 8.12814, 0.45846, 2.13448,
                                     0.36436, 0.76498, 0.07699, 0.66305, 0.06814, 0.026],
                                  [9.34763, 5.40322, 5.39348, 4.28531, 2.13769, 3.6986, 1.20349, 8.56544, 0.13936,
                                     1.06208, 0.07422, 0.42771, 0.07126, 0.20565, 0.58453, 0.13736, 0.01252],
                                  [8.17937, 9.0035, 7.0639, 8.01865, 4.38041, 1.88516, 8.56544, 1.47064, 0.39248, 2.12892, 0.2482, 1.47598,
                                     0.6615, 1.34006, 1.48759, 0.01198, 1.00754, 0.05332, 0.15599, 0.78827, 0.03313, 0.00021, 0.14672, 0.11168],
                                  [11.06131, 10.07051, 8.17937, 0.22206, 1.35006, 6.02977, 4.86441,
                                     1.21098, 4.3935, 0.03788, 0.08285, 0.03869, 0.79042],
                                  [9.34763, 6.59909, 3.99725, 2.53345, 2.13448, 1.49798, 6.02977, 2.75481,
                                     1.31229, 1.56642, 0.15447, 0.66883, 0.09997, 0.41825, 0.5336, 0.0035],
                                  [11.2293, 6.98258, 2.13769, 3.96605, 1.2324, 7.39112, 3.78908, 3.7543,
                                     0.76498, 0.12062, 0.8155, 0.40097, 0.38868, 1.00754, 0.00066],
                                  [9.93703, 9.63253, 5.42426, 4.33372, 8.01865, 7.39112, 7.72576, 1.9519, 1.10891, 0.06276,
                                     0.04753, 0.00067, 0.15146, 0.51246, 0.48527, 0.26072, 0.18282, 0.06992, 0.08612],
                                  [9.63253, 8.33909, 4.21163, 4.65033, 7.14305, 8.55588, 0.12062, 4.3935, 2.21196, 1.24497, 1.08011,
                                     0.73101, 0.7833, 1.59515, 1.48759, 1.03784, 0.66305, 0.00236, 0.5431, 0.10973, 0.29244],
                                  [11.2293, 4.15064, 5.39348, 2.53345, 4.92489, 8.55588, 1.88454, 0.48228,
                                     0.10084, 0.53964, 0.0112, 0.24242, 0.79042, 0.09615, 0.54134, 0.36573],
                                  [4.42903, 4.11413, 4.40323, 2.82301, 4.41618, 1.13609, 1.81567, 2.84804, 1.49798, 2.05146, 3.7543,
                                     0.10084, 1.11915, 0.70001, 0.00842, 0.37506, 1.15692, 0.60971, 0.48527, 0.5431, 0.00178, 0.05371],
                                  [10.4833, 3.34448, 5.97654, 0.91949, 4.33372, 2.84804, 1.04339,
                                     3.21424, 3.48983, 4.38041, 0.9712, 0.09133, 0.42771],
                                  [11.4364, 8.12814, 4.37255, 0.22206, 1.81567, 3.82073, 3.04708,
                                     7.14305, 0.7676, 2e-05, 1.06015, 1.56642, 0.51829, 0.41601],
                                  [3.88892, 4.42903, 3.00157, 1.62732, 0.00772, 0.45561,
                                     1.04339, 3.78908, 0.5688, 0.14031, 0.26072, 0.00858],
                                  [2.75984, 5.37884, 3.94835, 2.22882, 1.13609, 1.5404, 5.28538, 2.02063, 0.69734,
                                     0.29277, 3.31697, 0.09997, 0.04137, 0.50698, 0.44802, 0.09591, 0.00134],
                                  [10.40513, 4.78738, 3.34448, 2.90848, 9.90526, 0.99463, 0.01243, 3.31697, 0.12593, 1.67944, 1.11915,
                                     0.3781, 0.28145, 0.6615, 0.13929, 1.63415, 0.03869, 0.58174, 0.05334, 0.58453, 0.0035, 0.1485],
                                  [10.71848, 4.19973, 5.07466, 3.23877, 9.36811, 3.82073, 0.99463,
                                     0.25339, 0.01854, 0.2542, 4.94514, 0.03788, 1.08011, 1.11468, 0.37506],
                                  [3.09532, 5.37884, 4.52604, 1.7996, 4.41618, 9.36811, 0.6026, 1.99992, 0.74284,
                                     1.29612, 0.3004, 0.66883, 0.41601, 0.40663, 0.09627, 0.43702, 1.35609, 0.02646],
                                  [12.14056, 2.2294, 6.57561, 2.6832, 6.13752, 5.28538, 0.6026,
                                     1.3445, 1.61376, 4.65404, 0.7774, 0.09144, 1.63415],
                                  [10.09042, 9.90526, 7.0639, 7.7109, 7.70508, 1.35006, 0.24776, 4.65404, 1.01565, 1.88052, 1.11468, 1.12018,
                                     0.2257, 0.00957, 1.02868, 0.05994, 0.00321, 1.64323, 0.62449, 0.20565, 0.18282, 1.01676, 0.18548],
                                  [11.06131, 10.09042, 9.09844, 6.76629, 0.16104, 0.39248, 1.31229, 1.3445, 4.94514, 1.59515,
                                     0.96951, 3.38942, 1.35609, 0.85468, 0.54134, 1.17453, 0.38121, 0.08612, 0.417, 0.01044],
                                  [12.14056, 6.59909, 5.40322, 5.78798, 0.26519, 6.76629, 2.02063,
                                     1.99992, 0.48228, 0.45291, 1.01565, 0.00842, 0.58174, 0.03313],
                                  [10.84697, 11.66904, 4.468, 2.6832, 0.26519, 5.47628, 1.0387,
                                     0.62916, 1.2324, 0.30322, 0.11879, 0.60971, 0.15146],
                                  [11.66904, 0.03798, 9.29715, 7.52534, 7.70508, 7.72576, 5.55656, 1.61376, 0.68702, 0.31697, 0.45291,
                                     0.60611, 0.52468, 0.71038, 0.38868, 0.42338, 0.41503, 0.78827, 0.01907, 0.13736, 0.00178],
                                  [8.13113, 3.23877, 8.33909, 9.09844, 7.55571, 2.79523, 4.65273, 5.55656, 0.60361, 1.9519,
                                     2.17928, 0.62945, 1.88052, 1.85827, 0.40663, 0.74652, 0.09615, 0.05371, 0.00486],
                                  [10.84697, 5.78798, 2.2294, 0.03798, 3.2488, 4.92489, 3.96605,
                                     2.64935, 7.55571, 0.13936, 0.3004, 0.96951, 1.15692, 0.10973],
                                  [3.55475, 3.94835, 4.52604, 2.98298, 1.91749, 5.47628, 5.9785, 0.71321, 2.05146, 2.64935,
                                     0.01243, 1.77171, 1.25662, 0.01854, 0.98214, 0.68702, 0.40065, 0.00469, 0.74652],
                                  [10.40513, 6.35336, 1.84523, 0.91949, 5.9785, 7.52534, 0.69734, 4.37985,
                                     2.63837, 0.65031, 0.37433, 0.70001, 1.10891, 0.11879, 0.08499],
                                  [10.71848, 7.41596, 8.13113, 6.35336, 2.90848, 0.10138, 1.83389,
                                     2e-05, 0.73101, 0.08299, 0.71038, 0.2257, 0.51246, 0.28156],
                                  [2.75984, 3.09532, 3.55475, 2.82301, 0.12593],
                                  [0.88987, 4.12198, 5.07644, 1.74455, 0.01391, 1.47306, 1.5404,
                                     0.36436, 2.42174, 0.001, 3.97809, 0.53455, 1.71483, 0.58051, 0.0939],
                                  [7.55932, 5.45156, 1.18404, 1.4817, 0.01905, 1.48616, 3.29133, 2.64279,
                                     0.27438, 2.63837, 1.67944, 0.12841, 0.20652, 1.02868, 0.09591],
                                  [6.49443, 3.13, 4.74771, 7.41596, 4.19973, 3.29133, 2.76356, 0.93401, 0.19993, 2.20521,
                                     0.07242, 1.29612, 0.37433, 0.60361, 0.13929, 0.6757, 2e-05, 1.01676, 0.03623, 0.417],
                                  [4.24741, 5.07644, 0.12601, 1.18447, 0.43611, 2.98298, 2.22882,
                                     0.00275, 4.00975, 1.7996, 0.79359, 0.19993, 0.06445, 0.36735],
                                  [7.56053, 3.32342, 9.1491, 1.88118, 6.57561, 1.86539, 1.10301, 2.42174, 1.95251, 0.48669, 0.27907,
                                     2.1109, 0.89035, 0.12841, 1.06208, 0.30322, 0.50698, 0.05994, 0.42338, 0.05332, 0.12391, 0.1485],
                                  [11.29989, 9.1491, 6.48935, 1.64842, 1.48616, 0.41325, 7.7109,
                                     0.02703, 0.2645, 0.52468, 0.09144, 0.13993, 0.05334],
                                  [12.17242, 9.82351, 6.45737, 1.27925, 3.39598, 0.02703, 2.20521, 1.21098, 1.11866,
                                     0.2482, 0.51829, 0.20652, 0.05506, 0.0939, 3.38942, 1.64323, 0.5336, 0.026, 0.02646],
                                  [2.58928, 4.83415, 3.32342, 6.45737, 1.97368, 3.5018, 6.13752, 3.97809,
                                     0.36735, 0.91765, 0.19609, 0.44802, 0.43702, 1.17453, 0.03623, 0.00486],
                                  [3.45076, 5.4464, 4.28642, 4.18123, 3.34815, 0.32023, 0.00275, 0.76746, 1.50214,
                                     1.0387, 1.5114, 1.77171, 1.44669, 0.39504, 0.27137, 0.60611, 0.00495],
                                  [11.42534, 6.48935, 2.79277, 9.29715, 7.29315, 2.24711, 1.93318, 0.2587, 0.39504,
                                     0.89035, 0.08402, 1.12018, 1.85827, 0.01198, 0.07259, 0.6757, 0.08499, 0.28156],
                                  [12.75248, 5.61189, 4.82242, 3.93887, 1.50214, 4.21163, 2.57198,
                                     0.93401, 2.79523, 0.03291, 0.94801, 0.10788, 0.53964],
                                  [4.89012, 5.4464, 0.52253, 5.61189, 4.468, 0.75189, 0.11271, 3.5018, 3.2488,
                                     1.03503, 0.0, 0.48669, 0.06445, 1.25662, 0.7774, 0.52891, 2.17928, 0.01044],
                                  [4.24741, 0.96844, 0.16168, 0.01391, 1.99371,
                                     2.34654, 4.18123, 0.07136, 1.91749, 0.30756, 0.0],
                                  [5.45156, 6.84771, 1.29154, 5.85423, 2.76356, 3.12431, 4.37985, 0.00128,
                                     1.93318, 0.9712, 0.77778, 0.00495, 0.08299, 0.00469, 0.06276, 0.41503],
                                  [4.03485, 6.49443, 2.34394, 4.00975, 2.2375, 3.93887, 0.30756,
                                     0.10138, 0.25339, 0.27137, 0.74284, 0.52891, 0.40065, 0.62945],
                                  [0.44765, 0.61462, 0.88987, 0.06565, 0.16168, 0.12601, 0.74885]]]}

        actual = op_tools.neighbor_build.build_neighbor_wrapper(
            coord, box_length, op_settings, thread_num)
        actual['Delaunay'][1] = [[round(actual['Delaunay'][1][i][j], 5) for j in range(
            len(actual['Delaunay'][1][i]))] for i in range(len(actual['Delaunay'][1]))]
        actual['Delaunay'][2] = [[round(actual['Delaunay'][2][i][j], 5) for j in range(
            len(actual['Delaunay'][2][i]))] for i in range(len(actual['Delaunay'][2]))]
        self.assertEqual((expected == actual), True)


if __name__ == '__main__':
    unittest.main()
