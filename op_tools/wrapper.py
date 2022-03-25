# -*- coding: utf-8 -*-

import time
import numpy as np
from . import op_a_cnp
from . import op_t_msigma
from . import op_b_baa
from . import op_c_cpa
from . import op_d_nda
from . import op_f_afs
from . import op_h_aha
from . import op_i_top
from . import op_qw_spherical
from . import op_qw1_spherical
from . import op_qw2_spherical
from . import op_lqw_spherical
from . import op_s_local_onsager
from . import op_z_user_define
from . import misc
from . import neighbor_build


def param_check(op_settings, idx, init_value):
    if idx not in op_settings:
        op_settings[idx] = init_value
    return op_settings


def param_check_all(op_settings):

    op_settings = param_check(op_settings, 'ave_times', 0)
    # A
    if 'A' in op_settings['analysis_type']:
        op_settings = param_check(op_settings, 'm_in_A', [2])
        op_settings = param_check(op_settings, 'types_in_A', ['A'])
    # B
    if 'B' in op_settings['analysis_type']:
        op_settings = param_check(op_settings, 'm_in_B', [2])
        op_settings = param_check(op_settings, 'n_in_B', [1])
        op_settings = param_check(op_settings, 'phi_in_B', [0])
    # C
    # D
    # H
    if 'H' in op_settings['analysis_type']:
        op_settings = param_check(op_settings, 'b_in_H', 0)
        op_settings = param_check(op_settings, 'bin_in_H', [12])
        op_settings = param_check(op_settings, 'nu_in_H', [3])
    # I
    # Q W
    if 'Q' in op_settings['analysis_type'] or 'W' in op_settings['analysis_type']:
        op_settings = param_check(op_settings, 'l_in_Q', [4])
        op_settings = param_check(op_settings, 'b_in_Q', 0)
        op_settings = param_check(op_settings, 'p_in_Q', [0])
    # S
    if 'S' in op_settings['analysis_type']:
        op_settings = param_check(op_settings, 'n_in_S', [2])
    # T
    if 'T' in op_settings['analysis_type']:
        op_settings = param_check(op_settings, 'n_in_T', [2])
    return op_settings


def op_analyze_with_neighbor_list(coord, direct, box_length, NR_name, op_settings, n_list, nei_area, op_data, thread_num):
    """ Analyze structure
    :param method: method for analysis.
    Please see the details in readme file.
    :param coord: = [[0,0,0],[1,0,0]]
    :param direct: = [[1,0,0],[1,0,0]]
    :param box_length: = [10,10,10]
    :param NR_name: = 'N6'
    :param n_list: is neighbor list [[1],[0]]
    :param op_settings:
    :param thread_num:
    :return op_data: type(op_data) is dict.

    """

    op_settings = param_check_all(op_settings)
    op_temp = {}

    # common neighborhood parameter (CNP) A
    if 'A' in op_settings['analysis_type']:
        t_start = time.time()
        setting = {'ave_times': op_settings['ave_times'],
                   'm_in_A': op_settings['m_in_A'],
                   'op_types': op_settings['types_in_A']}
        op_temp['A_' + NR_name] = op_a_cnp.cnp_order_parameter(
            coord, box_length, setting, n_list, thread_num)
        t_end = time.time()
        print("# CNP A elap time ", t_end - t_start)

    # bond angle analysis (BAA) B
    if 'B' in op_settings['analysis_type']:
        t_start = time.time()
        setting = {'ave_times': op_settings['ave_times'],
                   'm': op_settings['m_in_B'],
                   'phi': op_settings['phi_in_B'],
                   'n': op_settings['n_in_B']}
        op_temp['B_' + NR_name] = op_b_baa.baa_order_parameter(
            coord, box_length, setting, n_list, thread_num)
        t_end = time.time()
        print("# BAA B elap time ", t_end - t_start)

    # centrometry parameter analysis (CPA) C
    if 'C' in op_settings['analysis_type']:
        t_start = time.time()
        setting = {'ave_times': op_settings['ave_times']}
        op_temp['C_' + NR_name] = op_c_cpa.cpa_order_parameter(
            coord, box_length, setting, n_list, thread_num)
        t_end = time.time()
        print("# CPA C elap time ", t_end - t_start)

    # neighbor distance analysis (NDA) D
    if 'D' in op_settings['analysis_type']:
        t_start = time.time()
        setting = {'ave_times': op_settings['ave_times'],
                   'func': op_settings['function']}
        op_temp['D_' + NR_name] = op_d_nda.nda_order_parameter(
            coord, box_length, setting, n_list, thread_num)
        t_end = time.time()
        print("# NDA D elap time ", t_end - t_start)

    # Angular Fourier Series like parameter (AFS) F
    if 'F' in op_settings['analysis_type']:
        t_start = time.time()
        setting = {'ave_times': op_settings['ave_times'],
                   'func': op_settings['function'],
                   'l_in_F': op_settings['l_in_F']}
        op_temp['F_' + NR_name] = op_f_afs.afs_order_parameter(
            coord, box_length, setting, n_list, thread_num)
        t_end = time.time()
        print("# AFS F elap time ", t_end - t_start)

    # angle histogram analysis (AHA) H
    if 'H' in op_settings['analysis_type']:
        t_start = time.time()
        setting = {'ave_times': op_settings['ave_times'],
                   'b_in_H': op_settings['b_in_H'],
                   'hist_num': op_settings['bin_in_H'],
                   'nu': op_settings['nu_in_H']
                   }
        op_temp['H_' + NR_name] = op_h_aha.aha_order_parameter(
            coord, box_length, setting, n_list, thread_num)
        t_end = time.time()
        print("# AHA H elap time ", t_end - t_start)

    # tetrahedral order parameter (TOP) I
    if 'I' in op_settings['analysis_type']:
        t_start = time.time()
        setting = {'ave_times': op_settings['ave_times']}
        op_temp['I_' + NR_name] = op_i_top.top_order_parameter(
            coord, box_length, setting, n_list, thread_num)
        t_end = time.time()
        print("# TOP I elap time ", t_end - t_start)

    # Spherical Order parameter Q or Wigner Order parameter W
    if 'Q' in op_settings['analysis_type'] or 'W' in op_settings['analysis_type']:
        t_start = time.time()
        setting = {'ave_times': op_settings['ave_times'],
                   'b_in_Q': op_settings['b_in_Q'],
                   'l_in_Q': op_settings['l_in_Q']}
        if 'Q' in op_settings['analysis_type']:
            op_temp['Q_' + NR_name] = op_qw_spherical.spherical_order_parameter(
                coord, direct, box_length, setting, n_list, thread_num)
            t_end = time.time()
            print("# Spherical Q elap time ", t_end - t_start)
        if 'W' in op_settings['analysis_type']:
            op_temp['W_' + NR_name] = op_qw_spherical.w_order_parameter(
                coord, direct, box_length, setting, n_list, thread_num)
            t_end = time.time()
            print("# Wigner W elap time ", t_end - t_start)

    # Spherical Order parameter Q1 or Wigner Order parameter W1
    if 'Q1' in op_settings['analysis_type'] or 'W1' in op_settings['analysis_type']:
        t_start = time.time()
        setting = {'ave_times': op_settings['ave_times'],
                   'b_in_Q': op_settings['b_in_Q'],
                   'l_in_Q': op_settings['l_in_Q'],
                   'p_in_Q': op_settings['p_in_Q']}
        if 'Q1' in op_settings['analysis_type']:
            op_temp['Q1_' + NR_name] = op_qw1_spherical.spherical_order_parameter(
                coord, box_length, setting, n_list, nei_area, thread_num)
            t_end = time.time()
            print("# Spherical Q1 elap time ", t_end - t_start)
        if 'W1' in op_settings['analysis_type']:
            op_temp['W1_' + NR_name] = op_qw1_spherical.spherical_order_parameter(
                coord, box_length, setting, n_list, nei_area, thread_num)
            t_end = time.time()
            print("# Wigner W1 elap time ", t_end - t_start)

    # Spherical Order parameter Q2 or Wigner Order parameter W2
    if 'Q2' in op_settings['analysis_type'] or 'W2' in op_settings['analysis_type']:
        t_start = time.time()
        setting = {'ave_times': op_settings['ave_times'],
                   'b_in_Q': op_settings['b_in_Q'],
                   'l_in_Q': op_settings['l_in_Q'],
                   'function_in_Q2': op_settings['function_in_Q2']}
        if 'Q2' in op_settings['analysis_type']:
            op_temp['Q2_' + NR_name] = op_qw2_spherical.spherical_order_parameter(
                coord, box_length, setting, n_list, nei_area, thread_num)
            t_end = time.time()
            print("# Spherical Q2 elap time ", t_end - t_start)
        if 'W2' in op_settings['analysis_type']:
            op_temp['W2_' + NR_name] = op_qw2_spherical.w_order_parameter(
                coord, box_length, setting, n_list, nei_area, thread_num)
            t_end = time.time()
            print("# Wigner W2 elap time ", t_end - t_start)

    # Local Spherical Order parameter Q or Local Wigner Order parameter W2
    if 'LQ' in op_settings['analysis_type'] or 'LW' in op_settings['analysis_type']:
        t_start = time.time()
        setting = {'ave_times': op_settings['ave_times'],
                   'b_in_Q': op_settings['b_in_Q'],
                   'l_in_Q': op_settings['l_in_Q'] }
        if 'LQ' in op_settings['analysis_type']:
            op_temp['LQ_' + NR_name] = op_lqw_spherical.spherical_order_parameter(
                coord, box_length, setting, n_list, thread_num)
            t_end = time.time()
            print("# Spherical LQ elap time ", t_end - t_start)
        if 'LW' in op_settings['analysis_type']:
            op_temp['LW_' + NR_name] = op_lqw_spherical.w_order_parameter(
                coord, box_length, setting, n_list, thread_num)
            t_end = time.time()
            print("# Wigner LW elap time ", t_end - t_start)

    # Onsager Order parameter S
    if 'S' in op_settings['analysis_type']:
        t_start = time.time()
        setting = {'ave_times': op_settings['ave_times'],
                   'n_in_S': op_settings['n_in_S']}
        op_temp['S_' + NR_name] = op_s_local_onsager.onsager_order_parameter(
            direct, setting, n_list, thread_num)
        t_end = time.time()
        print("# Onsager S elap time ", t_end - t_start)

    # McMillan Order parameter T
    if 'T' in op_settings['analysis_type']:
        t_start = time.time()
        setting = {'ave_times': op_settings['ave_times'],
                   'n_in_T': op_settings['n_in_T'],
                   'd_in_T': op_settings['d_in_T']}
        op_temp['T_' + NR_name] = op_t_msigma.mcmillan_order_parameter(
            coord, direct, box_length, setting, n_list, thread_num)
        t_end = time.time()
        print("# McMillan T elap time ", t_end - t_start)

    # User define order parameter
    if 'Z' in op_settings['analysis_type']:
        t_start = time.time()
        op_temp['Z_' + NR_name] = op_z_user_define.user_define_parameter(
            coord, direct, box_length, n_list)
        t_end = time.time()
        print("# User define Z elap time ", t_end - t_start)

    for iname in sorted(op_temp):
        for jname in sorted(op_temp[iname]):
            op_data[iname + '_' + jname] = op_temp[iname][jname]

    return op_data


def op_analyze(coord, direct, box_length, op_settings, thread_num):
    """ order parameter analyze
    :param method: method for analysis.  Please see the details in the manual.
    :param coord: = [[0,0,0],[1,0,0]]
    :param direct: = direction vector [[1,0,0],[1,0,0]] or quaternion [[1,0,0,0], [1,0,0,0]] or [] for no direction vector particle
    :param box_length: = [10,10,10]
    :param op_settings: settings for calculating order parameters
    :param thread_num:
    :return op_data:

    """

    coord = np.array(coord)
    direct = np.array(direct)

    # init direct
    if len(direct) == 0:
        direct = [[1, 0, 0] for i in range(len(coord))]
    if len(direct[0]) == 4:
        direct = misc.q_to_xyz(direct)
    direct = misc.vec_to_unit_vec(direct)

    # build neighbor list
    neighbors = neighbor_build.build_neighbor_wrapper(
        coord, box_length, op_settings, thread_num)

    # analyze
    op_data = {}
    for NR_name in sorted(neighbors):
        n_list = neighbors[NR_name][0]
        if NR_name == 'Delaunay':
            neighbor_area = neighbors[NR_name][2]
        else:
            neighbor_area = [[1 for j in n_list[i]] for i in range(len(coord))]
        op_data = op_analyze_with_neighbor_list(
            coord, direct, box_length, NR_name, op_settings, n_list, neighbor_area, op_data, thread_num)

    return op_data
