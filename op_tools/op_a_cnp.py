# -*- coding: utf-8 -*-

from multiprocessing import Pool, Array
import numpy as np
from . import misc


def calc_cnp_wrapper(args):
    [box_length, neighbor_list_ii, i_i, m_nei, op_types] = args

    op_temp = {}
    x_i = coord_1d[3*i_i: 3*i_i + 3]
    args = [box_length, neighbor_list_ii, x_i, max(m_nei)]
    nei_ij = misc.gen_neighbor_ijk(coord_1d, args)

    for now_m in m_nei:
        for op_type in op_types:
            sum_vec_m = [0, 0, 0]
            sum_r = 0.0
            for now_j, i_j in enumerate(neighbor_list_ii):
                x_j = coord_1d[3*i_j: 3*i_j + 3]

                sum_vec = [0.0, 0.0, 0.0]
                for now_k in range(now_m):
                    if now_k >= len(nei_ij[now_j]):
                        continue
                    i_k = nei_ij[now_j][now_k]
                    x_k = coord_1d[3 * i_k: 3*i_k + 3]
                    if op_type == 'A':
                        r_ik = misc.calc_delta(x_k, x_i, box_length)
                        r_jk = misc.calc_delta(x_k, x_j, box_length)
                        sum_vec = [sum_vec[i] + r_ik[i] + r_jk[i]
                                   for i in range(3)]
                    elif op_type == 'P' or op_type == 'N':
                        r_ij = misc.calc_delta(x_j, x_i, box_length)
                        r_kj = misc.calc_delta(x_j, x_k, box_length)
                        sum_vec = [sum_vec[i] + r_ij[i] + r_kj[i]
                                   for i in range(3)]

                if op_type == 'A' or op_type == 'P':
                    sum_r += np.dot(sum_vec, sum_vec)
                elif op_type == 'N':
                    sum_vec_m = [sum_vec_m[i] + sum_vec[i]
                                 for i in range(3)]

            if op_type == 'N':
                sum_r = np.dot(sum_vec_m, sum_vec_m)

            if len(neighbor_list_ii) != 0:
                now_op = sum_r / float(len(neighbor_list_ii))
            else:
                print('CAUTION! Particle has ', len(neighbor_list_ii),
                      ' nearby particle. Particle Number:', i_i+1)
                now_op = 0
            name = misc.naming(
                'a', [0, op_type, now_m])
            op_temp[name] = now_op

    return op_temp


def cnp_order_parameter(coord, box_length, setting, neighbor_list, thread_num):
    a_times = setting['ave_times']
    m_nei = setting['m_in_A']
    op_types = setting['op_types']

    # prepare parallel
    global coord_1d
    coord_1d = Array('d', misc.convert_3dim_to_1dim(coord), lock=False)

    now_pool = Pool(thread_num)
    args = [[box_length, neighbor_list[i_i],
             i_i, m_nei, op_types] for i_i in range(len(coord))]
    op_temp = now_pool.map(calc_cnp_wrapper, args)
    now_pool.close()

    del coord_1d

    op_value = misc.data_num_name_to_data_name_num(op_temp, len(coord))

    comb = [(op_type, m)
            for op_type in op_types for m in m_nei]
    for a_t in range(a_times):
        for op_type, m_nei in comb:
            name = misc.naming(
                'a', [a_t + 1, op_type, m_nei])
            name_old = misc.naming(
                'a', [a_t, op_type, m_nei])
            op_value[name] = misc.v_neighb_ave(
                neighbor_list, op_value[name_old])

    return op_value
