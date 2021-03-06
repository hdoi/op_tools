# -*- coding: utf-8 -*-

from multiprocessing import Pool, Array
import numpy as np
from . import misc


def calc_c_wrapper(args):
    [box_length, neighbor_list_ii, i_i, types, opp_mode] = args

    nei_ii = neighbor_list_ii
    op_temp = {}
    x_i = coord_1d[3 * i_i: 3*i_i + 3]

    comb = [(itype, imode) for itype in types for imode in opp_mode]
    half_N = int(len(nei_ii) / 2)

    for itype, imode in comb:
        sum_dist = 0
        if itype == 'half':
            target = half_N
        elif itype == 'all':
            target = len(nei_ii)

        for i_2 in range(target):
            i_j = nei_ii[i_2]
            x_j = coord_1d[3 * i_j: 3*i_j + 3]
            # imode = dist or angle
            i_k = misc.search_opposite_particle(coord_1d, nei_ii, x_i, i_j, x_j, box_length, imode)

            x_k = coord_1d[3 * i_k: 3 * i_k + 3]
            x_i_j = misc.calc_delta(x_j, x_i, box_length)
            x_i_k = misc.calc_delta(x_k, x_i, box_length)
            x_ij_ik = [x_i_j[i] + x_i_k[i] for i in range(3)]

            sum_dist += np.dot(x_ij_ik, x_ij_ik)

        name = misc.naming('c', [0, itype, imode])
        if target >= 1:
            op_temp[name] = sum_dist / half_N
        else:
            print('CAUTION! Particle has ', len(neighbor_list_ii), ' nearby particle. Particle Number:', i_i+1)
            op_temp[name] = 0

    return op_temp


def cpa_order_parameter(coord, box_length, setting, neighbor_list, thread_num):
    a_times = setting['ave_times']
    types = setting['types']
    modes = setting['modes']

    # prepare parallel
    global coord_1d
    coord_1d = Array('d', misc.convert_3dim_to_1dim(coord), lock=False)

    now_pool = Pool(thread_num)
    args = [[box_length, neighbor_list[i_i], i_i, types, modes]
            for i_i in range(len(coord))]
    op_val_temp = now_pool.map(calc_c_wrapper, args)
    now_pool.close()

    del coord_1d

    op_value = misc.data_num_name_to_data_name_num(op_val_temp, len(coord))

    # neighbor value averaging
    comb = [(a_t, itype, imode) for a_t in range(a_times) for itype in types for imode in modes]
    for a_t, itype, imode in comb:
        name = misc.naming('c', [a_t+1, itype, imode])
        name_old = misc.naming('c', [a_t, itype, imode])
        op_value[name] = misc.v_neighb_ave(neighbor_list, op_value[name_old])

    return op_value
