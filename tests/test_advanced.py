# -*- coding: utf-8 -*-

from .context import op_tools

import unittest
import math


class TestOrderParam(unittest.TestCase):

    """ test method of misc """

    def test_calc_delta(self):
        xi = [0, 0, 0]
        xj = [1, 1, 1]
        box_length = [10, 10, 10]

        expected = [-1, -1, -1]
        actual = op_tools.misc.calc_delta(xi, xj, box_length)
        self.assertEqual(all(expected == actual), True)

        xi = [0, 0, 0]
        xj = [6, 6, 6]
        box_length = [10, 10, 10]

        expected = [4,  4,  4]
        actual = op_tools.misc.calc_delta(xi, xj, box_length)
        self.assertEqual(all(expected == actual), True)

    def test_sort_by_distance(self):
        nei_list = [[0, 1]]
        nei_dist = [[2.0, 1.0]]

        expected = [[[1, 0]], [[1.0, 2.0]]]

        actual = op_tools.misc.sort_by_distance(
            nei_list, nei_dist)
        self.assertEqual((expected == actual), True)

    def test_angle(self):
        """ test method of angle """
        expected = (math.pi / 2.0)
        actual = op_tools.misc.angle([1, 0, 0], [0, 1, 1])
        self.assertEqual(expected, actual)

        expected = (math.pi / 2.0)
        actual = op_tools.misc.angle([1, 0, 0], [0, -1, -1])
        self.assertEqual(expected, actual)

        expected = (math.pi)
        actual = op_tools.misc.angle([1, 0, 0], [-1, 0, 0])
        self.assertEqual(expected, actual)

        expected = (math.pi)
        actual = op_tools.misc.angle([1, 0, 0], [-1, 0, 0])
        self.assertEqual(expected, actual)

    def test_convert_to_theta_phi(self):
        expected = {
            'dist': 2**(0.5), 'theta': math.pi / 2.0, 'phi': math.pi / 4.0}
        actual = op_tools.misc.convert_to_theta_phi([1, 1, 0])
        self.assertEqual(expected, actual)

    def test_gen_neighbor_ijk(self):
        coord_1d = [0, 0, 0, 1, 0, 0, 0.5, 0.5, 0, 1, 1, 0]
        box_length = [10.0, 10.0, 10.0]
        neighbor_list_ii = [1, 2, 3]
        x_i = [0, 0, 0]
        max_m = 2

        args = [box_length,
                neighbor_list_ii, x_i, max_m]

        expected = [[2, 3], [1, 3], [2, 1]]

        actual = op_tools.misc.gen_neighbor_ijk(coord_1d, args)
        self.assertEqual(expected, actual)

    def test_vec_to_unit_vec(self):
        xyz = [[-2,-2,0]]
        expected = [[-0.7071067811865475, -0.7071067811865475,0]]
        actual = op_tools.misc.vec_to_unit_vec(xyz)
        self.assertEqual(expected, actual)

if __name__ == '__main__':
    unittest.main()
