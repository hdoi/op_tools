# -*- coding: utf-8 -*-

import math
import numpy as np
import pyquaternion as pyquat


def convert_3dim_to_1dim(array3d):
    array = np.zeros(3 * len(array3d))
    for i_i, _ in enumerate(array3d):
        for i_j in range(3):
            array[3 * i_i + i_j] = array3d[i_i][i_j]
    return array


""" quartation to direction 3d vector """


def q_to_xyz(q_list):
    xyz = []
    for i, _ in enumerate(q_list):
        now_q = q_list[i]
        quat = pyquat.Quaternion(
            x=now_q[1], y=now_q[2], z=now_q[3], w=now_q[0])
        xyz.append(quat.rotate([1, 0, 0]))
    return xyz


def vec_to_unit_vec(xyz):
    for i, _ in enumerate(xyz):
        length = np.linalg.norm(xyz[i])
        if length == 0:
            xyz[i][0] = 1.0
        else:
            xyz[i] = [xyz[i][j]/length for j in range(3)]
    return xyz


def add_index_to_list(nei_ij, dist_ij, size, dist, index):
    if len(nei_ij) < size:
        nei_ij.append(index)
        dist_ij.append(dist)
    else:
        if max(dist_ij) > dist:
            idx = dist_ij.index(max(dist_ij))
            nei_ij[idx] = index
            dist_ij[idx] = dist
    return [nei_ij, dist_ij]


def sort_by_distance(nei_list, nei_dist):
    for i, _ in enumerate(nei_list):
        temp_list = []
        temp_dist = []
        for j in range(len(nei_list[i])):
            idx = nei_dist[i].index(min(nei_dist[i]))
            temp_list.append(nei_list[i][idx])
            temp_dist.append(min(nei_dist[i]))
            nei_list[i].pop(idx)
            nei_dist[i].pop(idx)
        nei_list[i] = temp_list
        nei_dist[i] = temp_dist
    return [nei_list, nei_dist]


""" plane perpendicular to direction vector through point """


def gen_z_plane(point, direct):
    a_v = direct[0]
    b_v = direct[1]
    c_v = direct[2]
    d_v = -a_v * point[0] - b_v * point[1] - c_v * point[2]
    return [a_v, b_v, c_v, d_v]


def gen_neighbor_ij(coord_1d, args):
    [box_length, neighbor_list_ii, x_i, i_j, m_neighbor] = args

    x_j = coord_1d[3*i_j: 3*i_j + 3]

    i_j_nei = []
    i_j_dist = []
    for i_k in neighbor_list_ii:
        if i_j == i_k:
            continue
        x_k = coord_1d[3*i_k: 3*i_k+3]
        dist = distance_ik_jk(x_i, x_j, box_length, x_k)
        [i_j_nei, i_j_dist] = add_index_to_list(
            i_j_nei, i_j_dist, m_neighbor, dist, i_k)

    [i_j_nei, i_j_dist] = sort_by_distance([i_j_nei], [i_j_dist])
    i_j_nei = i_j_nei[0]
    i_j_dist = i_j_dist[0]

    return i_j_nei


def gen_neighbor_ijk(coord_1d, args):
    [box_length, neighbor_list_ii, x_i, max_m] = args

    neighbor_ijk = []
    for i_j in neighbor_list_ii:
        args = [box_length, neighbor_list_ii, x_i, i_j, max_m]
        i_j_nei = gen_neighbor_ij(coord_1d, args)
        neighbor_ijk.append(i_j_nei)

    return neighbor_ijk


def v_neighb_ave(neighbor_list, val):
    if isinstance(val[0], type([])):
        val_ave = []  # [[1,2,3],[1,2,3], ... ]
        for i_i, _ in enumerate(neighbor_list):
            part = [0 for _ in range(len(val[i_i]))]
            for i_j in range(len(val[i_i])):
                for inei in neighbor_list[i_i] + [i_i]:
                    part[i_j] += val[inei][i_j] / float(
                        len(neighbor_list[i_i]) + 1)
            val_ave.append(part)
    elif isinstance(val[0], type(np.array([]))):
        val_ave = []  # [[1,2,3],[1,2,3], ... ]
        for i_i, _ in enumerate(neighbor_list):
            part = [0 for _ in range(len(val[i_i]))]
            for i_j in range(len(val[i_i])):
                for inei in neighbor_list[i_i] + [i_i]:
                    part[i_j] += val[inei][i_j] / float(
                        len(neighbor_list[i_i]) + 1)
            val_ave.append(part)
        val_ave = np.array(val_ave)
    else:
        val_ave = []
        for i_i, _ in enumerate(neighbor_list):
            part = []
            for inei in neighbor_list[i_i] + [i_i]:
                part.append(val[inei])
            val_ave.append(np.average(part))
    return val_ave


def angle(v_1, v_2):
    return math.acos(np.dot(v_1, v_2) / (np.linalg.norm(v_1) * np.linalg.norm(v_2)))


def distance_ik_jk(x_i, x_j, box_length, x_k):
    x_ik = calc_delta(x_k, x_i, box_length)
    x_jk = calc_delta(x_k, x_j, box_length)
    distance = np.linalg.norm(x_ik) + np.linalg.norm(x_jk)
    return distance


def search_opposite_particle(coord_1d, neighbor_list_ii, x_i, i_j, x_j, box_length, imode):
    x_i_j = calc_delta(x_j, x_i, box_length)
    x_j_opposite = [x_i[i] - x_i_j[i] for i in range(3)]

    if imode == 'dist':
        nearest_i_k = 1000
        nearest_distnace = 10000000.0
        for i_k in neighbor_list_ii:
            if i_k == i_j:
                continue
            x_k = coord_1d[3*i_k: 3*i_k + 3]
            x_j_o_k = calc_delta(x_k, x_j_opposite, box_length)
            distance = np.linalg.norm(x_j_o_k)
            if distance <= nearest_distnace:
                nearest_distnace = distance
                nearest_i_k = i_k
    elif imode == 'angle':
        nearest_i_k = 1000
        nearest_angle = -10000000.0
        for i_k in neighbor_list_ii:
            if i_k == i_j:
                continue
            x_k = coord_1d[3*i_k: 3*i_k + 3]
            x_i_k = calc_delta(x_k, x_i, box_length)
            angle_jik = angle(x_i_j, x_i_k)

            if angle_jik >= nearest_angle:
                nearest_angle = angle_jik
                nearest_i_k = i_k

    return nearest_i_k


def plane_point_distance(plane_var, box_length, point):
    a_v = plane_var[0]
    b_v = plane_var[1]
    c_v = plane_var[2]
    d_v = plane_var[3]

    distance = [0, 0, 0]
    for i_i in range(-1, 2):
        p_temp = [point[i] + i_i * box_length[i] for i in range(3)]
        x_v = p_temp[0]
        y_v = p_temp[1]
        z_v = p_temp[2]
        distance[i_i] = abs(a_v * x_v + b_v * y_v + c_v * z_v + d_v) / \
            math.sqrt(a_v**2 + b_v**2 + c_v**2)

    return min(distance)


def calc_theta_phi(x_i, x_j, box_length):
    delta = calc_delta(x_i, x_j, box_length)
    pol = convert_to_theta_phi(delta)
    return [pol['theta'], pol['phi']]


def calc_delta(x_end, x_start, box_length):
    delta = np.array([x_end[i] - x_start[i] for i in range(3)])
    for i in range(3):
        if delta[i] < -box_length[i] / 2.0:
            delta[i] += box_length[i]
        elif delta[i] >= box_length[i] / 2.0:
            delta[i] -= box_length[i]
    return delta


def convert_to_theta_phi(xyz):
    dist = np.linalg.norm(xyz)
    theta = math.acos(xyz[2] / dist)
    phi = math.atan2(xyz[1], xyz[0])

    return {'dist': dist, 'theta': theta, 'phi': phi}


def data_num_name_to_data_name_num(a_dict, num_part):
    # data[i_i][name] => data[name][i_i]
    b_dict = {}
    for name in sorted(a_dict[0]):
        a_temp = []
        for i_i in range(num_part):
            a_temp.append(a_dict[i_i][name])
        b_dict[name] = a_temp

    return b_dict


def naming(mode, arg):
    if mode == 'a':
        [a_t, op_type, m_nei] = arg
        name = 'a=' + str(a_t) + '_type=' + str(op_type) + '_m=' + str(m_nei)

    if mode == 'b':
        [a_t, m_fac, phi, n_pow] = arg
        name = 'a=' + str(a_t) + '_m=' + str(m_fac) + '_phi=' + str(
            phi) + '_n=' + str(n_pow)

    if mode == 'c':
        [a_t, itype, imode] = arg
        name = 'a=' + str(a_t) + '_type=' + str(itype) + '_mode=' + str(imode)

    if mode == 'd':
        [a_t, f_1, f_2, f_3] = arg
        name = 'a=' + str(a_t) + '_f1=' + str(f_1) + '_f2=' + str(f_2) + '_f3=' + str(f_3)

    if mode == 'f':
        [a_t, f_1, f_2, l_nei] = arg
        name = 'a=' + str(a_t) + '_f1=' + str(f_1) + '_f2=' + str(f_2) + '_l=' + str(l_nei)

    if mode == 'h':
        [a_t, b_t, ibin] = arg
        name = 'a=' + str(a_t) + '_b=' + str(b_t) + '_bin=' + str(ibin)
    
    if mode == 'i':
        [a_t ] = arg
        name = 'a=' + str(a_t)

    if mode == 'q' or mode == 'w':
        [l_sph, a_t, b_t] = arg
        name = 'l=' + str(l_sph) + '_a=' + str(a_t) + '_b=' + str(b_t)

    if mode == 'q2' or mode == 'w2':
        [l_sph, f_1, a_t, b_t] = arg
        name = 'l=' + str(l_sph) + '_f1=' + str(f_1) + \
            '_a=' + str(a_t) + '_b=' + str(b_t)

    if mode == 's':
        [a_t, n_leg] = arg
        name = 'a=' + str(a_t) + '_n=' + str(n_leg)

    if mode == 't':
        [a_t, dist_layers, n_leg] = arg
        name = 'a=' + str(a_t) + '_n=' + str(n_leg) + '_z=' + str(dist_layers)

    return name
