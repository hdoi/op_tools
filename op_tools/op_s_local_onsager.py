# -*- coding: utf-8 -*-

import numpy as np
from multiprocessing import Pool, Array
from . import misc
from scipy.special import legendre


def calc_order_param(direct, n_leg, ref_vec=None):
    # second Legendre polynomial or Onsarger's order parameter
    # direct = [ [0,1,1], [1,2,3], ... ]

    # legendre function
    legend_fac = list(legendre(n_leg))

    if ref_vec == None:
        ref_vec = [0, 0, 0]
        for idirect in direct:
            temp = np.array(idirect)
            if np.dot(ref_vec, temp) < 0.0:
                ref_vec -= temp
            else:
                ref_vec += temp
        ref_vec = ref_vec / np.sqrt(np.dot(ref_vec, ref_vec))

    order_param = []
    for idirect in direct:
        # length = np.sqrt(np.dot(x_coord,x_coord))
        i_dir = np.array(idirect)
        i_dir = i_dir / np.linalg.norm(i_dir)
        cos_theta = np.dot(ref_vec, i_dir)

        temp = 0
        for i in range(len(legend_fac)):
            # n = 2 : legend_fac = [1.5, 0.0, -0.5]
            temp += legend_fac[i]*cos_theta**(n_leg-i)

        temp = round(temp, 12)
        order_param.append(temp)

    return [order_param, ref_vec]


def calc_s_wrapper(args):
    [neighbor_list_ii, i_i, n_legendre] = args

    direct_ii = direct_1d[3 * i_i: 3 * i_i + 3]
    # order parameter
    part_direct = []
    for i_j in neighbor_list_ii:
        direct_i_j = direct_1d[3 * i_j: 3*i_j + 3]
        part_direct.append(direct_i_j)

    op_temp = {}
    for n_leg in n_legendre:
        [order_param, rev_vec] = calc_order_param(part_direct, n_leg, direct_ii)
        name = misc.naming('s', [0, n_leg])
        if len(order_param) != 0:  # no neighbor
            op_temp[name] = np.average(order_param)
        else:
            op_temp[name] = 0.0
    return op_temp


def onsager_order_parameter(direct, setting, neighbor_list, thread_num):
    a_times = setting['ave_times']
    n_legendre = setting['n_in_S']

    global direct_1d
    direct_1d = Array('d', misc.convert_3dim_to_1dim(direct), lock=False)

    now_pool = Pool(thread_num)
    args = [[neighbor_list[i_i], i_i, n_legendre] for i_i in range(len(direct))]
    op_val_temp = now_pool.map(calc_s_wrapper, args)
    now_pool.close()

    del direct_1d
    op_data = misc.data_num_name_to_data_name_num(op_val_temp, len(direct))

    for a_t in range(a_times):
        for n_leg in n_legendre:
            name = misc.naming('s', [a_t+1, n_leg])
            name_old = misc.naming('s', [a_t, n_leg])
            op_data[name] = misc.v_neighb_ave(neighbor_list, op_data[name_old])

    return op_data
