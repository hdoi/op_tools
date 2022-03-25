# -*- coding: utf-8 -*-

import math
from multiprocessing import Pool, Array
from . import misc


def calc_i_wrapper(args):
    [box_length, neighbor_list_ii, i_i] = args

    op_temp = {}
    sum_cos = 0.0
    x_i = coord_1d[3 * i_i: 3*i_i + 3]

    for i_2 in range(len(neighbor_list_ii) - 1):
        i_j = neighbor_list_ii[i_2]
        x_j = coord_1d[3 * i_j: 3*i_j + 3]
        for i_3 in range(i_2 + 1, len(neighbor_list_ii)):
            i_k = neighbor_list_ii[i_3]
            x_k = coord_1d[3 * i_k: 3*i_k + 3]

            x_i_j = misc.calc_delta(x_j, x_i, box_length)
            x_i_k = misc.calc_delta(x_k, x_i, box_length)
            try:
                theta = misc.angle(x_i_j, x_i_k)
            except ValueError:
                theta = 0.0
            if theta >= math.pi:
                theta -= math.pi

            sum_cos += (math.cos(theta) + 1/3.0)**2
    op_i = 1 - (3.0/8.0)*sum_cos

    name = misc.naming('c', [0])
    op_temp[name] = op_i

    return op_temp


def top_order_parameter(coord, box_length, setting, neighbor_list, thread_num):
    a_times = setting['ave_times']

    # prepare parallel
    global coord_1d
    coord_1d = Array('d', misc.convert_3dim_to_1dim(coord), lock=False)

    now_pool = Pool(thread_num)
    args = [[box_length, neighbor_list[i_i], i_i]
            for i_i in range(len(coord))]
    op_val_temp = now_pool.map(calc_i_wrapper, args)
    now_pool.close()

    del coord_1d

    op_value = misc.data_num_name_to_data_name_num(op_val_temp, len(coord))

    # neighbor histogram averaging
    for a_t in range(a_times):
        name = misc.naming('c', [a_t+1])
        name_old = misc.naming('c', [a_t])
        op_value[name] = misc.v_neighb_ave(
            neighbor_list, op_value[name_old])

    return op_value
