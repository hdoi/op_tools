# -*- coding: utf-8 -*-

from . import misc
from . import lib_qw as lib
import numpy as np
from multiprocessing import Pool, Array


def calc_q_wrapper(args):
    [box_length, neighbor_list_ii, i_i, l_list, nei_area] = args

    q_func_temp = {}
    for l_sph in l_list:
        name = misc.naming('q', [l_sph, 0, 0])
        x_i = coord_1d[3 * i_i: 3*i_i + 3]

        # neighbor
        q_temp = np.array([0 + 0j for i in range(2 * l_sph + 1)])
        sum_area = np.sum(nei_area)
        num_nei = len(neighbor_list_ii)
        for i in range(len(neighbor_list_ii)):
            i_j = neighbor_list_ii[i]
            x_j = coord_1d[3 * i_j: 3*i_j + 3]
            [theta, phi] = misc.calc_theta_phi(x_i, x_j, box_length)
            area_weight = num_nei*(nei_area[i]/sum_area)
            q_l = lib.calc_q_weighted(l_sph, theta, phi, area_weight)

            for i_k in range(2 * l_sph + 1):
                q_temp[i_k] += q_l[i_k]

        for i_k in range(2 * l_sph + 1):
            q_temp[i_k] = q_temp[i_k] / (float(len(neighbor_list_ii)))

        q_func_temp[name] = q_temp

    return q_func_temp


def calc_spherical_order_parameter(calc_type, coord, box_length, setting, neighbor_list, neighbor_area, thread_num):
    # [Q_N]_l_a_b
    a_times = setting['ave_times']
    b_times = setting['b_in_Q']
    l_list = setting['l_in_Q']

    # calc spherical function
    # prepare parallel
    global coord_1d
    coord_1d = Array('d', misc.convert_3dim_to_1dim(coord), lock=False)

    now_pool = Pool(thread_num)
    args = [[box_length, neighbor_list[i_i], i_i, l_list, neighbor_area[i_i]]
            for i_i in range(len(coord))]
    q_func_temp = now_pool.map(calc_q_wrapper, args)
    now_pool.close()

    del coord_1d

    q_func = misc.data_num_name_to_data_name_num(q_func_temp, len(coord))

    # calc function average
    comb = [(l_sph, b_t) for l_sph in l_list for b_t in range(b_times)]

    for l_sph, b_t in comb:
        name = misc.naming('q', [l_sph, 0, b_t+1])
        name_old = misc.naming('q', [l_sph, 0, b_t])
        q_func[name] = misc.v_neighb_ave(neighbor_list, q_func[name_old])

    # func to value
    op_data = {}
    if calc_type == 'Q':
        for l_sph in l_list:
            for b_t in range(b_times + 1):
                name = misc.naming('q', [l_sph, 0, b_t])
                q_val = []
                for i_i in range(len(coord)):
                    q_val.append(lib.func_to_value(l_sph, q_func[name][i_i]))
                op_data[name] = q_val
    elif calc_type == 'W':
        for l_sph in l_list:
            wigner3j = lib.gen_wigner3j(l_sph)
            for b_t in range(b_times + 1):
                name = misc.naming('w', [l_sph, 0, b_t])
                w_val = []
                for i_i in range(len(coord)):
                    w_val.append(lib.func_to_value_wigner(l_sph, wigner3j, q_func[name][i_i]))
                op_data[name] = w_val

    # neighbor value averaging
    comb = [(l_sph, a_t, b_t)
            for l_sph in l_list
            for a_t in range(a_times)
            for b_t in range(b_times+1)]
    for l_sph, a_t, b_t in comb:
        name = misc.naming('q', [l_sph, a_t+1, b_t])
        name_old = misc.naming('q', [l_sph, a_t, b_t])
        op_data[name] = misc.v_neighb_ave(neighbor_list, op_data[name_old])

    return op_data


def spherical_order_parameter(coord, box_length, setting, neighbor_list, neighbor_area, thread_num):
    op_data = calc_spherical_order_parameter(
        'Q', coord, box_length, setting, neighbor_list, neighbor_area, thread_num)
    return op_data


def w_order_parameter(coord, box_length, setting, neighbor_list, neighbor_area, thread_num):
    op_data = calc_spherical_order_parameter(
        'W', coord, box_length, setting, neighbor_list, neighbor_area, thread_num)
    return op_data
