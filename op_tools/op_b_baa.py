# -*- coding: utf-8 -*-

import math
from multiprocessing import Pool, Array
from . import misc


def calc_baa_wrapper(args):
    [box_length, neighbor_list_ii, i_i,
        m_l, phi_l, n_l] = args

    comb = [(m_fac, phi, n_pow) for m_fac in m_l for phi in phi_l for n_pow in n_l]

    b_list = {}
    for m_fac, phi, n_pow in comb:
        x_i = coord_1d[3*i_i: 3*i_i + 3]
        op_temp = 0
        for i_2 in range(len(neighbor_list_ii) - 1):
            i_j = neighbor_list_ii[i_2]
            x_j = coord_1d[3 * i_j: 3*i_j + 3]
            for i3 in range(i_2 + 1, len(neighbor_list_ii)):
                i_k = neighbor_list_ii[i3]
                x_k = coord_1d[3 * i_k : 3 * i_k + 3]

                x_i_j = misc.calc_delta(x_j, x_i, box_length)
                x_ik = misc.calc_delta(x_k, x_i, box_length)
                try:
                    theta = misc.angle(x_i_j, x_ik)
                except ValueError:
                    theta = 0.0

                op_temp += (math.cos(m_fac * theta + phi))**n_pow
        n_1 = float(len(neighbor_list_ii))
        if n_1 >= 2:
            op_temp = op_temp / (n_1 * (n_1 - 1) / 2)
        else:
            print('CAUTION! Particle has ', len(neighbor_list_ii),
                  ' nearby particle. Particle Number:', i_i+1)
            op_temp = 0

        name = misc.naming('b', [0, m_fac, phi, n_pow])
        b_list[name] = op_temp

    return b_list


def baa_order_parameter(coord, box_length, setting, neighbor_list, thread_num):
    a_times = setting['ave_times']
    m_l = setting['m']
    phi_l = setting['phi']
    n_l = setting['n']

    # prepare parallel
    global coord_1d
    coord_1d = Array('d', misc.convert_3dim_to_1dim(coord), lock=False)

    # calc b
    now_pool = Pool(thread_num)
    args = [[box_length, neighbor_list[i_i], i_i, m_l, phi_l, n_l]
            for i_i in range(len(coord))]
    op_val_temp = now_pool.map(calc_baa_wrapper, args)
    now_pool.close()

    del coord_1d

    op_value = misc.data_num_name_to_data_name_num(op_val_temp, len(coord))

    # neighbor value averaging
    comb = [(m_fac, phi, n_pow) for m_fac in m_l for phi in phi_l for n_pow in n_l]

    for a_t in range(a_times):
        for m_fac, phi, n_pow in comb:
            name = misc.naming('b', [a_t+1, m_fac, phi, n_pow])
            name_old = misc.naming('b', [a_t, m_fac, phi, n_pow])
            op_value[name] = misc.v_neighb_ave(neighbor_list, op_value[name_old])

    return op_value
