# -*- coding: utf-8 -*-

import numpy as np
from multiprocessing import Pool, Array
from . import misc


def calc_d_wrapper(args):
    [box_length, neighbor_list_ii, i_i, func] = args

    comb = [(f_1, f_2, f_3)
            for f_1 in range(len(func))
            for f_2 in range(len(func))
            for f_3 in range(len(func))]

    op_temp = {}
    for f_1, f_2, f_3 in comb:
        name = misc.naming('d', [0, f_1, f_2, f_3])

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
                x_k = coord_1d[3 * i_k: 3* i_k + 3]
                x_ik = misc.calc_delta(x_k, x_i, box_length)
                xjk = misc.calc_delta(x_k, x_j, box_length)
                dik = np.linalg.norm(x_ik)
                djk = np.linalg.norm(xjk)

                d_sum += func[f_1](di_j) * func[f_2](dik) * func[f_3](djk)
        if N >= 2:
            op_temp[name] = d_sum / (N * (N - 1) / 2)
        else:
            print('CAUTION! Particle has ', len(neighbor_list_ii), ' nearby particle. Particle Number:', i_i+1)
            op_temp[name] = 0

    return op_temp


def nda_order_parameter(coord, box_length, setting, neighbor_list, thread_num):
    a_times = setting['ave_times']
    func = setting['func']

    # prepare parallel
    global coord_1d
    coord_1d = Array('d', misc.convert_3dim_to_1dim(coord), lock=False)

    now_pool = Pool(thread_num)
    args = [[box_length, neighbor_list[i_i], i_i, func]
            for i_i in range(len(coord))]
    op_val_temp = now_pool.map(calc_d_wrapper, args)
    now_pool.close()

    del coord_1d

    op_value = misc.data_num_name_to_data_name_num(op_val_temp, len(coord))

    # neighbor value averaging
    comb = [(f_1, f_2, f_3)
            for f_1 in range(len(func))
            for f_2 in range(len(func))
            for f_3 in range(len(func))]

    for a_t in range(a_times):
        for f_1, f_2, f_3 in comb:
            name = misc.naming('d', [a_t+1, f_1, f_2, f_3])
            name_old = misc.naming(
                'd', [a_t, f_1, f_2, f_3])
            op_value[name] = misc.v_neighb_ave(
                neighbor_list, op_value[name_old])

    return op_value
