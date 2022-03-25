#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
sys.path.insert( 0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import op_tools
import numpy as np


def read_xyz(filename):
    f = open(filename, 'r')
    lines = f.readlines()

    num_part = int(lines[0])

    bl = lines[1].split()
    box_length = [float(bl[i]) for i in range(3)]

    coord = []
    for i in range(num_part):
        temp = lines[i+2].split()
        coord.append([float(temp[1]), float(temp[2]), float(temp[3])])

    return [box_length, coord]


def f1(j, voronoi_area_list, distance_list):
    weight = distance_list[j] / np.sum(distance_list)
    return weight


if __name__ == '__main__':
    [box_length, coord] = read_xyz('sample_data/LJ/bcc.xyz')
    direct = []
    op_settings = {'neighbor': [12],
                   'radius': [1.5],
                   'Delaunay': ['standard'],
                   'ave_times': 1,
                   'm_in_A': [2],
                   'types_in_A': ['A', 'P', 'N'],
                   'analysis_type': ['A']}
    op_data = op_tools.op_analyze(
        coord, direct, box_length, op_settings, 1)
    for i1, v1 in op_data.items():
        print(i1)

    op_settings = {'neighbor': [12],
                   'radius': [1.5],
                   'Delaunay': ['standard'],
                   'ave_times': 1,
                   'm_in_B': [2],
                   'phi_in_B': [0],
                   'n_in_B': [1, 2],
                   'analysis_type': ['B']}
    op_data = op_tools.op_analyze(
        coord, direct, box_length, op_settings, 1)
    for i1, v1 in op_data.items():
        print(i1)

    op_settings = {
        'neighbor': [12],
        'radius': [1.5],
        'Delaunay': ['standard'],
        'ave_times': 1,
        'analysis_type': ['C']
    }

    op_data = op_tools.op_analyze(
        coord, direct, box_length, op_settings, 1)
    for i1, v1 in op_data.items():
        print(i1)

    def f_1(r):
        return r
    op_settings = {
        'neighbor': [12],
        'radius': [1.5],
        'Delaunay': ['standard'],
        'ave_times': 1,
        'function': [f_1],
        'analysis_type': ['D']
    }

    op_data = op_tools.op_analyze(
        coord, direct, box_length, op_settings, 1)
    for i1, v1 in op_data.items():
        print(i1)

    op_settings = {
        'neighbor': [12],
        'radius': [1.5],
        'Delaunay': ['standard'],
        'ave_times': 1,
        'l_in_F': [1],
        'function': [f_1],
        'analysis_type': ['F']
    }
    op_data = op_tools.op_analyze(
        coord, direct, box_length, op_settings, 1)
    for i1, v1 in op_data.items():
        print(i1)

    op_settings = {
        'neighbor': [12],
        'radius': [1.5],
        'Delaunay': ['standard'],
        'ave_times': 1,
        'b_in_H': 1,
        'bin_in_H': [24],
        'nu_in_H': [3],
        'analysis_type': ['H']}

    op_data = op_tools.op_analyze(
        coord, direct, box_length, op_settings, 1)
    for i1, v1 in op_data.items():
        print(i1)

    op_settings = {
        'neighbor': [4],
        'radius': [1.5],
        'Delaunay': ['standard'],
        'ave_times': 1,
        'analysis_type': ['I']}

    op_data = op_tools.op_analyze(
        coord, direct, box_length, op_settings, 1)
    for i1, v1 in op_data.items():
        print(i1)

    op_settings = {
        'neighbor': [12],
        'radius': [1.5],
        'Delaunay': ['standard'],
        'ave_times': 1,
        'l_in_Q': [4],
        'b_in_Q': 1,
        'p_in_Q': [0],
        'analysis_type': ['Q', 'W']}

    op_data = op_tools.op_analyze(
        coord, direct, box_length, op_settings, 1)
    for i1, v1 in op_data.items():
        print(i1)

    op_settings = {
        'Delaunay': ['standard'],
        'ave_times': 1,
        'l_in_Q': [4],
        'b_in_Q': 1,
        'p_in_Q': [0],
        'analysis_type': ['Q1', 'W1']}

    op_data = op_tools.op_analyze(
        coord, direct, box_length, op_settings, 1)
    for i1, v1 in op_data.items():
        print(i1)

    op_settings = {
        'neighbor': [12],
        'radius': [1.5],
        'Delaunay': ['standard'],
        'ave_times': 1,
        'l_in_Q': [4],
        'b_in_Q': 1,
        'p_in_Q': [0],
        'function_in_Q2': [f1],
        'analysis_type': ['Q2', 'W2']}

    op_data = op_tools.op_analyze(
        coord, direct, box_length, op_settings, 1)
    for i1, v1 in op_data.items():
        print(i1)

    op_settings = {
        'neighbor': [12],
        'radius': [1.5],
        'Delaunay': ['standard'],
        'ave_times': 1,
        'l_in_Q': [4],
        'b_in_Q': 1,
        'p_in_Q': [0],
        'analysis_type': ['LQ', 'LW']}

    op_data = op_tools.op_analyze(
        coord, direct, box_length, op_settings, 1)
    for i1, v1 in op_data.items():
        print(i1)

    op_settings = {
        'neighbor': [12],
        'radius': [1.5],
        'Delaunay': ['standard'],
        'ave_times': 1,
        'n_in_S': [2],
        'analysis_type': ['S']
    }

    op_data = op_tools.op_analyze(
        coord, direct, box_length, op_settings, 1)
    for i1, v1 in op_data.items():
        print(i1)

    op_settings = {
        'neighbor': [12],
        'radius': [1.5],
        'Delaunay': ['standard'],
        'ave_times': 1,
        'd_in_T': [1.0],
        'n_in_T': [2],
        'analysis_type': ['T']
    }

    op_data = op_tools.op_analyze(
        coord, direct, box_length, op_settings, 1)
    for i1, v1 in op_data.items():
        print(i1)

    op_settings = {
        'neighbor': [12],
        'radius': [1.5],
        'Delaunay': ['standard'],
        'analysis_type': ['Z']
    }

    op_data = op_tools.op_analyze(
        coord, direct, box_length, op_settings, 1)
    for i1, v1 in op_data.items():
        print(i1)

    def f_1(r):
        return r
    op_settings = {
        'neighbor': [8],
        'radius': [1.5],
        'Delaunay': ['standard'],
        'ave_times': 1,
        # A
        'op_types': ['A', 'P', 'N'],
        'm_in_A': [2, 4],
        # B
        'm_in_B': [2],
        'n_in_B': [1, 2],
        'phi_in_B': [0],
        # D
        'function': [f_1],
        # F
        'l_in_F': [1],
        # H
        'b_in_H': 1,
        'bin_in_H': [24],
        'nu_in_H': [3],
        # I
        # Q W
        'b_in_Q': 1,
        'l_in_Q': [2, 4, 6],
        'p_in_Q': [0],
        # S
        'n_in_S': [2],
        # T
        'n_in_T': [2],
        'd_in_T': [1.0],
        'analysis_type': ['A', 'B', 'C', 'D', 'F', 'H', 'I', 'Q', 'W', 'S', 'T']}

    op_data = op_tools.op_analyze(
        coord, direct, box_length, op_settings, 1)
    for i1, v1 in op_data.items():
        print(i1)
