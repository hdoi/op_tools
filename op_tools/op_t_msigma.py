# -*- coding: utf-8 -*-

import math
from multiprocessing import Pool, Array
import numpy as np
from . import misc
from scipy.special import legendre


def calc_t_wrapper(args):
    [box_length, neighbor_list_ii, i_i, layer_list, n_legendre] = args

    comb = [(n_leg) for n_leg in n_legendre]

    op_temp = {}
    for n_leg in comb:
        direct_ii = direct_1d[3 * i_i: 3* i_i + 3]
        x_i = coord_1d[3 * i_i: 3*i_i + 3]

        if np.linalg.norm(direct_ii) == 0.0:
            plane_var = misc.gen_z_plane(x_i, [0, 0, 1])
        else:
            plane_var = misc.gen_z_plane(x_i, direct_ii)

        sum_r = [0 for i in range(len(layer_list))]
        for i_j in neighbor_list_ii:
            direct_i_j = direct_1d[3 * i_j: 3*i_j + 3]
            x_j = coord_1d[3 * i_j: 3*i_j + 3]

            cos_theta = np.dot(direct_ii, direct_i_j) / \
                (np.linalg.norm(direct_ii)*np.linalg.norm(direct_i_j))
            # legendre function
            legend_fac = list(legendre(n_leg))

            s_part = 0
            for i in range(len(legend_fac)):
                # n = 2 : legend_fac = [1.5, 0.0, -0.5]
                s_part += legend_fac[i]*cos_theta**(n_leg-i)

            dist_from_plane = misc.plane_point_distance(plane_var, box_length, x_j)

            for i_k, dist_layers in enumerate(layer_list):
                cos_part = math.cos( 2.0 * math.pi * dist_from_plane / dist_layers)
                sum_r[i_k] += cos_part * s_part

        for i_k, dist_layers in enumerate(layer_list):
            if not neighbor_list_ii:
                sum_r[i_k] = 0.0
            else:
                sum_r[i_k] = sum_r[i_k] / float(len(neighbor_list_ii))

            name = misc.naming('t', [0, dist_layers, n_leg])
            op_temp[name] = round(sum_r[i_k],12)

    return op_temp


def mcmillan_order_parameter(coord, direct, box_length, setting, neighbor_list, thread_num):
    a_times = setting['ave_times']
    layer_list = setting['d_in_T']
    n_legendre = setting['n_in_T']

    # prepare parallel
    global coord_1d
    coord_1d = Array('d', misc.convert_3dim_to_1dim(coord), lock=False)

    global direct_1d
    direct_1d = Array('d', misc.convert_3dim_to_1dim(direct), lock=False)

    now_pool = Pool(thread_num)
    args = [[box_length, neighbor_list[i_i],
             i_i, layer_list, n_legendre] for i_i in range(len(coord))]
    op_val_temp = now_pool.map(calc_t_wrapper, args)
    now_pool.close()

    del coord_1d
    del direct_1d

    op_data = misc.data_num_name_to_data_name_num(op_val_temp, len(coord))

    comb = [(dist_layers, n_leg)
            for dist_layers in layer_list
            for n_leg in n_legendre]
    
    for a_t in range(a_times):
        for dist_layers, n_leg in comb:
            name = misc.naming('t', [a_t+1, dist_layers, n_leg])
            name_old = misc.naming( 't', [a_t, dist_layers, n_leg])
            op_data[name] = misc.v_neighb_ave(neighbor_list, op_data[name_old])

    return op_data
