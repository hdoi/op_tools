# -*- coding: utf-8 -*-

import math
from multiprocessing import Pool, Array
import numpy as np
from . import misc


def calc_f_wrapper(args):
    [box_length, neighbor_list_ii, i_i, func, l_list] = args

    comb = [(f_1, f_2, l)
            for f_1 in range(len(func))
            for f_2 in range(len(func))
            for l in l_list]

    op_temp = {}
    for f_1, f_2, l in comb:
        name = misc.naming('f', [0, f_1, f_2, l])

        x_i = coord_1d[3 * i_i: 3*i_i + 3]

        N = len(neighbor_list_ii)
        d_sum = 0.0
        for i_2 in range(N - 1):
            i_j = neighbor_list_ii[i_2]
            x_j = coord_1d[3 * i_j: 3*i_j + 3]
            x_i_j = misc.calc_delta(x_j, x_i, box_length)
            di_j = np.linalg.norm(x_i_j)

            for i3 in range(i_2 + 1, N):
                i_k = neighbor_list_ii[i3]
                x_k = coord_1d[3 * i_k: 3 * i_k + 3]
                x_ik = misc.calc_delta(x_k, x_i, box_length)
                di_k = np.linalg.norm(x_ik)

                try:
                    theta = misc.angle(x_i_j, x_ik)
                except ValueError:
                    theta = 0.0
                if theta >= math.pi:
                    theta -= math.pi

                d_sum += func[f_1](di_j) * func[f_2](di_k) * math.cos(l*theta)
        if N >= 2:
            op_temp[name] = d_sum / (N * (N - 1) / 2)
        else:
            print('CAUTION! Particle has ', len(neighbor_list_ii),
                  ' nearby particle. Particle Number:', i_i+1)
            op_temp[name] = 0

    return op_temp


def afs_order_parameter(coord, box_length, setting, neighbor_list, thread_num):
    a_times = setting['ave_times']
    l_list = setting['l_in_F']
    func = setting['func']

    # prepare parallel
    global coord_1d
    coord_1d = Array('d', misc.convert_3dim_to_1dim(coord), lock=False)

    now_pool = Pool(thread_num)
    args = [[box_length, neighbor_list[i_i], i_i, func, l_list]
            for i_i in range(len(coord))]
    op_val_temp = now_pool.map(calc_f_wrapper, args)
    now_pool.close()

    del coord_1d

    op_value = misc.data_num_name_to_data_name_num(op_val_temp, len(coord))

    # neighbor value averaging
    comb = [(f_1, f_2, l)
            for f_1 in range(len(func))
            for f_2 in range(len(func))
            for l in l_list]
    for a_t in range(a_times):
        for f_1, f_2, l in comb:
            name = misc.naming('f', [a_t+1, f_1, f_2, l])
            name_old = misc.naming('f', [a_t, f_1, f_2, l])
            op_value[name] = misc.v_neighb_ave(
                neighbor_list, op_value[name_old])

    return op_value
