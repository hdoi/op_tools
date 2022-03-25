# -*- coding: utf-8 -*-

from . import misc
from . import lib_qw as lib
import numpy as np
import math
from multiprocessing import Pool, Array


def calc_q_body(coord_ii, coord_ij, args):
    [box_length, neighbor_list_ii, i_i, l_list, nei_area, func_list] = args

    comb = [(l_sph, func)
            for l_sph in l_list for func in func_list]

    q_func_temp = {}
    for l_sph, func in comb:
        name = misc.naming('q2', [l_sph, func.__name__, 0, 0])

        x_i = coord_ii

        dist_list = []
        for j in range(len(neighbor_list_ii)):
            x_j = coord_ij[j]
            delta = misc.calc_delta(x_i, x_j, box_length)
            dist_list.append(np.linalg.norm(delta))

        # neighbor
        q_temp = np.array([0 + 0j for i in range(2 * l_sph + 1)])
        for j in range(len(neighbor_list_ii)):
            x_j = coord_ij[j]
            [theta, phi] = misc.calc_theta_phi(x_i, x_j, box_length)
            weight = func(j, nei_area, dist_list)
            q_l = lib.calc_q_weighted(l_sph, theta, phi, weight)

            for i_k in range(2 * l_sph + 1):
                q_temp[i_k] += q_l[i_k]

        q_func_temp[name] = q_temp

    return q_func_temp


def calc_q_wrapper(args):
    [box_length, neighbor_list_ii, i_i, l_list, nei_area, func_list] = args

    coord_ii = coord_1d[3 * i_i: 3*i_i + 3]

    coord_ij = []
    for j in range(len(neighbor_list_ii)):
        i_j = neighbor_list_ii[j]
        coord_ij.append(coord_1d[3*i_j: 3*i_j+ 3])

    q_func_temp = calc_q_body(coord_ii, coord_ij, args)
    return q_func_temp


def calc_spherical_order_parameter(calc_type, coord, box_length, setting, neighbor_list, neighbor_area, thread_num):
    # [Q_N]_l_a_b
    a_times = setting['ave_times']
    b_times = setting['b_in_Q']
    l_list = setting['l_in_Q']
    func_list = setting['function_in_Q2']

    # calc spherical function
    # prepare parallel
    global coord_1d
    coord_1d = Array('d', misc.convert_3dim_to_1dim(coord), lock=False)

    now_pool = Pool(thread_num)
    args = [[box_length, neighbor_list[i_i], i_i, l_list, neighbor_area[i_i],
             func_list] for i_i in range(len(coord))]
    q_func_temp = now_pool.map(calc_q_wrapper, args)
    now_pool.close()

    del coord_1d

    q_func = misc.data_num_name_to_data_name_num(q_func_temp, len(coord))

    # calc function average
    comb = [(l_sph, func, b_t)
            for l_sph in l_list
            for func in func_list
            for b_t in range(b_times)]

    for l_sph, func, b_t in comb:
        name = misc.naming( 'q2', [l_sph, func.__name__, 0, b_t+1])
        name_old = misc.naming( 'q2', [l_sph, func.__name__, 0, b_t])
        q_func[name] = misc.v_neighb_ave(neighbor_list, q_func[name_old])

    # func to value
    if calc_type == 'Q':
        comb = [(l_sph, func)
                for l_sph in l_list
                for func in func_list]
        op_data = {}
        for b_t in range(b_times + 1):
            for l_sph, func in comb:
                name = misc.naming( 'q2', [l_sph, func.__name__, 0, b_t])
                q_val = []
                for i_i in range(len(coord)):
                    q_val.append(lib.func_to_value(l_sph, q_func[name][i_i]))
                op_data[name] = q_val
    elif calc_type == 'W':
        comb = [(func ) for func in func_list]

        op_data = {}
        for l_sph in l_list:
            wigner3j = lib.gen_wigner3j(l_sph)
            for b_t in range(b_times + 1):
                for func in comb:
                    name = misc.naming( 'w2', [l_sph, func.__name__, 0, b_t])
                    w_val = []
                    for i_i in range(len(coord)):
                        w_val.append(lib.func_to_value_wigner(
                            l_sph, wigner3j, q_func[name][i_i]))
                    op_data[name] = w_val

    # neighbor value averaging
    comb = [(l_sph, func, a_t, b_t)
            for l_sph in l_list
            for func in func_list
            for a_t in range(a_times)
            for b_t in range(b_times+1)]
    for l_sph, func, a_t, b_t in comb:
        name = misc.naming( 'q2', [l_sph, func.__name__, a_t+1, b_t])
        name_old = misc.naming( 'q2', [l_sph, func.__name__, a_t, b_t])
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
