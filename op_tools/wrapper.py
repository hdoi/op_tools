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
from . import op_qw2_spherical
from . import op_lqw_spherical
from . import op_s_local_onsager
from . import op_z_user_define
from . import misc
from . import neighbor_build


def param_check(op_settings, idx, init_value):
    if idx not in op_settings:
        op_settings[idx] = init_value
        print("WARNING! Parameter :", idx, " was not found.")
        print("Default parameter ", init_value, " was set in ", '"'+idx+'".')
    return op_settings


def elap_time(name, time):
    print("# ", name, "elap time", round(time, 5), ' (s)')
    return


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

    op_temp = {}

    op_settings = param_check(op_settings, 'ave_times', 0)
    # common neighborhood parameter (CNP) A
    if 'A' in op_settings['analysis_type']:
        op_settings = param_check(op_settings, 'm_in_A', [2])
        op_settings = param_check(op_settings, 'types_in_A', ['A'])

        t_start = time.time()
        setting = {'ave_times': op_settings['ave_times'],
                   'm_in_A': op_settings['m_in_A'],
                   'op_types': op_settings['types_in_A']}
        op_temp['A_' + NR_name] = op_a_cnp.cnp_order_parameter(
            coord, box_length, setting, n_list, thread_num)
        t_end = time.time()
        elap_time("CNP A", t_end - t_start)

    # bond angle analysis (BAA) B
    if 'B' in op_settings['analysis_type']:
        op_settings = param_check(op_settings, 'm_in_B', [2])
        op_settings = param_check(op_settings, 'n_in_B', [1])
        op_settings = param_check(op_settings, 'phi_in_B', [0])

        t_start = time.time()
        setting = {'ave_times': op_settings['ave_times'],
                   'm': op_settings['m_in_B'],
                   'phi': op_settings['phi_in_B'],
                   'n': op_settings['n_in_B']}
        op_temp['B_' + NR_name] = op_b_baa.baa_order_parameter(
            coord, box_length, setting, n_list, thread_num)
        t_end = time.time()
        elap_time("BAA B", t_end - t_start)

    # centrometry parameter analysis (CPA) C
    if 'C' in op_settings['analysis_type']:
        op_settings = param_check(op_settings, 'types_in_C', ['orig'])
        op_settings = param_check(op_settings, 'modes_in_C', ['dist'])

        t_start = time.time()
        setting = {'ave_times': op_settings['ave_times'],
                   'types': op_settings['types_in_C'],
                   'modes': op_settings['modes_in_C']}
        op_temp['C_' + NR_name] = op_c_cpa.cpa_order_parameter(
            coord, box_length, setting, n_list, thread_num)
        t_end = time.time()
        elap_time("CPA C", t_end - t_start)

    # neighbor distance analysis (NDA) D
    if 'D' in op_settings['analysis_type']:
        t_start = time.time()
        setting = {'ave_times': op_settings['ave_times'],
                   'func': op_settings['function']}
        op_temp['D_' + NR_name] = op_d_nda.nda_order_parameter(
            coord, box_length, setting, n_list, thread_num)
        t_end = time.time()
        elap_time("NDA D", t_end - t_start)

    # Angular Fourier Series like parameter (AFS) F
    if 'F' in op_settings['analysis_type']:
        t_start = time.time()
        setting = {'ave_times': op_settings['ave_times'],
                   'func': op_settings['function'],
                   'l_in_F': op_settings['l_in_F']}
        op_temp['F_' + NR_name] = op_f_afs.afs_order_parameter(
            coord, box_length, setting, n_list, thread_num)
        t_end = time.time()
        elap_time("AFS F", t_end - t_start)

    # angle histogram analysis (AHA) H
    if 'H' in op_settings['analysis_type']:
        op_settings = param_check(op_settings, 'b_in_H', 0)
        op_settings = param_check(op_settings, 'bin_in_H', [12])
        op_settings = param_check(op_settings, 'nu_in_H', [3])

        t_start = time.time()
        setting = {'ave_times': op_settings['ave_times'],
                   'b_in_H': op_settings['b_in_H'],
                   'hist_num': op_settings['bin_in_H'],
                   'nu': op_settings['nu_in_H']
                   }
        op_temp['H_' + NR_name] = op_h_aha.aha_order_parameter(
            coord, box_length, setting, n_list, thread_num)
        t_end = time.time()
        elap_time("AHA H", t_end - t_start)

    # tetrahedral order parameter (TOP) I
    if 'I' in op_settings['analysis_type']:
        t_start = time.time()
        setting = {'ave_times': op_settings['ave_times']}
        op_temp['I_' + NR_name] = op_i_top.top_order_parameter(
            coord, box_length, setting, n_list, thread_num)
        t_end = time.time()
        elap_time("TOP I", t_end - t_start)

    # Spherical Order parameter Q or Wigner Order parameter W
    if 'Q' in op_settings['analysis_type'] or 'W' in op_settings['analysis_type']:
        op_settings = param_check(op_settings, 'l_in_Q', [4])
        op_settings = param_check(op_settings, 'b_in_Q', 0)

        t_start = time.time()
        setting = {'ave_times': op_settings['ave_times'],
                   'b_in_Q': op_settings['b_in_Q'],
                   'l_in_Q': op_settings['l_in_Q']}
        if 'Q' in op_settings['analysis_type']:
            op_temp['Q_' + NR_name] = op_qw_spherical.spherical_order_parameter(
                coord, direct, box_length, setting, n_list, thread_num)
            t_end = time.time()
            elap_time("Spherical Q", t_end - t_start)
        if 'W' in op_settings['analysis_type']:
            op_temp['W_' + NR_name] = op_qw_spherical.w_order_parameter(
                coord, direct, box_length, setting, n_list, thread_num)
            t_end = time.time()
            elap_time("Wigner W", t_end - t_start)

    # Spherical Order parameter Q2 or Wigner Order parameter W2
    if 'Q2' in op_settings['analysis_type'] or 'W2' in op_settings['analysis_type']:
        op_settings = param_check(op_settings, 'l_in_Q', [4])
        op_settings = param_check(op_settings, 'b_in_Q', 0)

        t_start = time.time()
        setting = {'ave_times': op_settings['ave_times'],
                   'b_in_Q': op_settings['b_in_Q'],
                   'l_in_Q': op_settings['l_in_Q'],
                   'function_in_Q2': op_settings['function_in_Q2']}
        if 'Q2' in op_settings['analysis_type']:
            op_temp['Q2_' + NR_name] = op_qw2_spherical.spherical_order_parameter(
                coord, box_length, setting, n_list, nei_area, thread_num)
            t_end = time.time()
            elap_time("Spherical Q2", t_end - t_start)

        if 'W2' in op_settings['analysis_type']:
            op_temp['W2_' + NR_name] = op_qw2_spherical.w_order_parameter(
                coord, box_length, setting, n_list, nei_area, thread_num)
            t_end = time.time()
            elap_time("Wigner W2", t_end - t_start)

    # Local Spherical Order parameter Q or Local Wigner Order parameter W
    if 'LQ' in op_settings['analysis_type'] or 'LW' in op_settings['analysis_type']:
        op_settings = param_check(op_settings, 'l_in_Q', [4])
        op_settings = param_check(op_settings, 'b_in_Q', 0)

        t_start = time.time()
        setting = {'ave_times': op_settings['ave_times'],
                   'b_in_Q': op_settings['b_in_Q'],
                   'l_in_Q': op_settings['l_in_Q']}
        if 'LQ' in op_settings['analysis_type']:
            op_temp['LQ_' + NR_name] = op_lqw_spherical.spherical_order_parameter(
                coord, box_length, setting, n_list, thread_num)
            t_end = time.time()
            elap_time("Spherical LQ", t_end - t_start)
        if 'LW' in op_settings['analysis_type']:
            op_temp['LW_' + NR_name] = op_lqw_spherical.w_order_parameter(
                coord, box_length, setting, n_list, thread_num)
            t_end = time.time()
            elap_time("Wigner LW", t_end - t_start)

    # Onsager Order parameter S
    if 'S' in op_settings['analysis_type']:
        op_settings = param_check(op_settings, 'n_in_S', [2])

        t_start = time.time()
        setting = {'ave_times': op_settings['ave_times'],
                   'n_in_S': op_settings['n_in_S']}
        op_temp['S_' + NR_name] = op_s_local_onsager.onsager_order_parameter(
            direct, setting, n_list, thread_num)
        t_end = time.time()
        elap_time("Onsager S", t_end - t_start)

    # McMillan Order parameter T
    if 'T' in op_settings['analysis_type']:
        op_settings = param_check(op_settings, 'n_in_T', [2])
        op_settings = param_check(op_settings, 'd_in_T', [1.0])

        t_start = time.time()
        setting = {'ave_times': op_settings['ave_times'],
                   'n_in_T': op_settings['n_in_T'],
                   'd_in_T': op_settings['d_in_T']}
        op_temp['T_' + NR_name] = op_t_msigma.mcmillan_order_parameter(
            coord, direct, box_length, setting, n_list, thread_num)
        t_end = time.time()
        elap_time("McMillan T", t_end - t_start)

    # User define order parameter
    if 'Z' in op_settings['analysis_type']:
        t_start = time.time()
        op_temp['Z_' + NR_name] = op_z_user_define.user_define_parameter(
            coord, direct, box_length, n_list)
        t_end = time.time()
        elap_time("User define Z", t_end - t_start)

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
