# -*- coding: utf-8 -*-

import math
from multiprocessing import Pool, Array
from scipy.fftpack import fft
import numpy as np
from . import misc


def histogram_normalize(hist):
    sum_hist = np.sum(hist)
    hist = [hist[i]/sum_hist for i in range(len(hist))]
    return hist


def calc_h_wrapper(args):
    [box_length, neighbor_list_ii, i_i, h_num] = args

    op_temp = {}
    # init histogram
    hist_temp = []  # hist_temp[bin_num][ibin]
    for i_k, _ in enumerate(h_num):
        h_temp2 = [0 for i in range(h_num[i_k])]
        hist_temp.append(h_temp2)

    x_i = coord_1d[3 * i_i: 3*i_i + 3]

    n_list = len(neighbor_list_ii)
    if n_list >= 2:
        for i_2 in range(len(neighbor_list_ii) - 1):
            i_j = neighbor_list_ii[i_2]
            x_j = coord_1d[3 * i_j: 3*i_j + 3]
            for i_3 in range(i_2 + 1, len(neighbor_list_ii)):
                i_k = neighbor_list_ii[i_3]
                x_k = coord_1d[3 * i_k: 3*i_k + 3]

                x_i_j = misc.calc_delta(x_j, x_i, box_length)
                x_ik = misc.calc_delta(x_k, x_i, box_length)
                try:
                    theta = misc.angle(x_i_j, x_ik)
                except ValueError:
                    theta = 0.0
                if theta >= math.pi:
                    theta -= math.pi

                for i_k, _ in enumerate(h_num):
                    h_i = h_num[i_k]
                    now_i = int(h_i * theta / math.pi)
                    hist_temp[i_k][now_i] += 1.0 / float(n_list * (n_list - 1) / 2)
    else:
        print('CAUTION! Particle has ', len(neighbor_list_ii),
              ' nearby particle. Particle Number:', i_i+1)
        for i_k, _ in enumerate(h_num):
            hist_temp[i_k][0] = 1.0

    for i_k, _ in enumerate(h_num):
        name = misc.naming('h', [0, 0, h_num[i_k]])
        op_temp[name] = hist_temp[i_k]

    return op_temp


def aha_order_parameter(coord, box_length, setting, neighbor_list, thread_num):
    a_times = setting['ave_times']
    b_times = setting['b_in_H']
    h_num = setting['hist_num']
    nu = setting['nu']

    # prepare parallel
    global coord_1d
    coord_1d = Array('d', misc.convert_3dim_to_1dim(coord), lock=False)

    now_pool = Pool(thread_num)
    args = [[box_length, neighbor_list[i_i], i_i, h_num] for i_i in range(len(coord))]
    op_val_temp = now_pool.map(calc_h_wrapper, args)
    now_pool.close()

    del coord_1d

    h_hist = misc.data_num_name_to_data_name_num(op_val_temp, len(coord))

    # neighbor histogram averaging
    for b_t in range(b_times):
        for i_k, _ in enumerate(h_num):
            name = misc.naming('h', [0, b_t+1, h_num[i_k]])
            name_old = misc.naming('h', [0, b_t, h_num[i_k]])
            h_hist[name] = misc.v_neighb_ave(
                neighbor_list, h_hist[name_old])

    # FFT
    h_data_part_nu = {}
    for b_t in range(b_times + 1):
        for i_k, _ in enumerate(h_num):
            name = misc.naming('h', [0, b_t, h_num[i_k]])
            g_list = []
            for i_i, _ in enumerate(coord):
                g_func = fft(histogram_normalize(h_hist[name][i_i]))
                g_power = np.abs(g_func)**2
                power = []
                for inu in nu:
                    try:
                        power.append(g_power[inu])
                    except IndexError as e:
                        power.append(0)
                g_list.append(power)
            h_data_part_nu[name] = g_list

    op_value = {}
    for b_t in range(b_times + 1):
        for i_k, _ in enumerate(h_num):
            for i_l, _ in enumerate(nu):
                inu = nu[i_l]
                name = misc.naming('h', [0, b_t, h_num[i_k]])
                name_h = name + '_nu=' + str(inu)

                op_value[name_h] = [h_data_part_nu[name][i_i][i_l]
                                    for i_i in range(len(coord))]

    for a_t in range(a_times):
        for b_t in range(b_times + 1):
            for i_k, _ in enumerate(h_num):
                for i_l, _ in enumerate(nu):
                    name = misc.naming('h', [a_t+1, b_t, h_num[i_k]]) + '_nu=' + str(inu)
                    name_old = misc.naming('h', [a_t, b_t, h_num[i_k]]) + '_nu=' + str(inu)
                    op_value[name] = misc.v_neighb_ave(
                        neighbor_list, op_value[name_old])

    return op_value
