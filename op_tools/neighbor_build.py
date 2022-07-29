# -*- coding: utf-8 -*-

import time
from multiprocessing import Pool, Array
from scipy.spatial import Voronoi
import sys
import math
import numpy as np
from . import misc
from . import wrapper


class SmallRadiusError(Exception):

    def __str__(self):
        return 'neighbor radius too small'


def calc_thresh(box_length, part_num, target_num, safe_factor):
    density = float(part_num) / (box_length[0] * box_length[1] * box_length[2])
    target_r = (target_num / (density * (4.0 / 3.0) * math.pi))**(1.0 / 3.0)

    return safe_factor * target_r


def build_neighbor_cell(cell, cell_size):
    # input  : [0,0,0]
    # output : if cell_size == [4,4,4] , [-1,0,0] => [3,0,0], [4,0,0] =>
    # [0,0,0]
    neighbor = [[cell[0] + ix, cell[1] + iy, cell[2] + iz]
                for ix in range(-1, 2)
                for iy in range(-1, 2)
                for iz in range(-1, 2)]
    for i in range(3**3):
        for j in range(3):
            if neighbor[i][j] == -1:
                neighbor[i][j] = cell_size[j] - 1
            elif neighbor[i][j] == cell_size[j]:
                neighbor[i][j] = 0
    return neighbor


def wrapper_cell_calc(args):
    [i_i, cell_length, cell_size, cell_list, box_length, condition] = args

    nei_list = []
    nei_dist = []

    coord_ii = coord_1d[3 * i_i: 3*i_i + 3]

    cell = coord_to_cell_num(coord_ii, cell_length)
    neighbor = build_neighbor_cell(cell, cell_size)
    for inei in neighbor:
        for i_j in cell_list[inei[0]][inei[1]][inei[2]]:
            if i_i < i_j:
                coord_i_j = coord_1d[3 * i_j: 3*i_j+3]
                dist = np.linalg.norm(
                    misc.calc_delta(coord_ii, coord_i_j, box_length))
                if condition['mode'] == 'thresh':
                    if dist <= condition['dist']:
                        nei_list.append(i_j)
                        nei_dist.append(dist)
                elif condition['mode'] == 'neighbor':
                    if len(nei_list) < condition['num']:
                        nei_list.append(i_j)
                        nei_dist.append(dist)
                    else:
                        if max(nei_dist) > dist:
                            idx = nei_dist.index(max(nei_dist))
                            nei_list[idx] = i_j
                            nei_dist[idx] = dist
    return [nei_list, nei_dist]


def coord_to_cell_num(coord, cell_length):
    inum = [int(coord[i] / cell_length[i]) for i in range(3)]
    return inum


def add_num_dist(nei_list, nei_dist, num, i_j, dist):
    # add i_j to nei_list and nei_dist
    if len(nei_list) < num:
        nei_list.append(i_j)
        nei_dist.append(dist)
    else:
        if max(nei_dist) > dist:
            idx = nei_dist.index(max(nei_dist))
            nei_list[idx] = i_j
            nei_dist[idx] = dist
    return [nei_list, nei_dist]


def build_cell(coord, box_length, thresh_dist):
    cell_length = [0, 0, 0]
    cell_size = [0, 0, 0]
    for i in range(3):
        cell_size[i] = int(box_length[i] / thresh_dist)
        cell_length[i] = box_length[i] / float(cell_size[i])

    cell_list = \
        [[[[] for _ in range(cell_size[2])] for _ in range(cell_size[1])]
         for _ in range(cell_size[0])]

    for i, _ in enumerate(coord):
        for j in range(3):
            coord[i][j] = check_boundary_condition(coord[i][j], box_length[j])

        inum = coord_to_cell_num(coord[i], cell_length)
        cell_list[inum[0]][inum[1]][inum[2]].append(i)

    return [cell_list, cell_length, cell_size]


def check_boundary_condition(x, box_length):
    if x < 0.0:
        x = x - math.floor(x / box_length)*box_length
    if x >= box_length:
        x = x - math.floor(x / box_length)*box_length
    return x

def build_neighbor_list(coord, box_length, condition, thread_num):
    """ building neighbor list
    :param coord: = [[0,0,0],[1,0,0]]
    :param box_length: = [10,10,10]
    :param condition: =
    {'mode' : 'thresh' or 'neighbor',
        'neighbor' is number of neighborhood particles,
        'dist' : is radii of neighborhood particles. }
    :return [neighbor_list, neidhbor_distance]: is new neighbor list
    """
    t_start = time.time()
    [cell_list, cell_length, cell_size] = build_cell(
        coord, box_length, condition['dist'])

    if min(cell_size) <= 2:
        nei_list = [[] for i in range(len(coord))]
        nei_dist = [[] for i in range(len(coord))]
        for i_i in range(len(coord) - 1):
            for i_j in range(i_i + 1, len(coord)):
                dist = np.linalg.norm(
                    misc.calc_delta(coord[i_i], coord[i_j], box_length))
                if condition['mode'] == 'thresh':
                    if dist <= condition['dist']:
                        nei_list[i_i].append(i_j)
                        nei_dist[i_i].append(dist)
                        nei_list[i_j].append(i_i)
                        nei_dist[i_j].append(dist)
                elif condition['mode'] == 'neighbor':
                    [nei_list[i_i], nei_dist[i_i]] = \
                        add_num_dist(
                            nei_list[i_i], nei_dist[i_i], condition['num'], i_j, dist)
                    [nei_list[i_j], nei_dist[i_j]] = \
                        add_num_dist(
                            nei_list[i_j], nei_dist[i_j], condition['num'], i_i, dist)
        [nei_list, nei_dist] = misc.sort_by_distance(nei_list, nei_dist)
        return [nei_list, nei_dist]

    # prepare parallel
    global coord_1d
    coord_1d = Array('d', misc.convert_3dim_to_1dim(coord), lock=False)

    now_pool = Pool(thread_num)
    args = [[i, cell_length, cell_size, cell_list, box_length, condition]
            for i in range(len(coord))]
    out_data = now_pool.map(wrapper_cell_calc, args)
    now_pool.close()

    del coord_1d

    nei_list = [[] for i in range(len(coord))]
    nei_dist = [[] for i in range(len(coord))]
    for i in range(len(coord)):
        nei_list[i] = out_data[i][0]
        nei_dist[i] = out_data[i][1]

    for i, _ in enumerate(nei_list):
        for j, _ in enumerate(nei_list[i]):
            now_j = nei_list[i][j]
            if i < now_j:
                if condition['mode'] == 'thresh':
                    nei_list[now_j].append(i)
                    nei_dist[now_j].append(nei_dist[i][j])
                elif condition['mode'] == 'neighbor':
                    [nei_list[now_j], nei_dist[now_j]] = \
                        add_num_dist(nei_list[now_j], nei_dist[now_j],
                                     condition['num'], i, nei_dist[i][j])

    [nei_list, nei_dist] = misc.sort_by_distance(nei_list, nei_dist)

    # check
    if condition['mode'] == 'neighbor':
        if len(nei_list) < condition['num']:
            print('# neighbor num too big. you require ',
                  condition['num'], ' neighbors. But there are ', len(nei_list), 'particles.')
            sys.exit(1)
        for i, _ in enumerate(nei_list):
            if len(nei_list[i]) < condition['num']:
                print('# radius too small. you require ', condition['num'],
                      ' neighbors. But there are ', len(nei_list[i]), 'neighbors.')
                sys.exit(1)

    t_end = time.time()
    wrapper.elap_time("neighbor build", t_end - t_start)
    return [nei_list, nei_dist]


def mod_neighbor_list(nei_list, nei_dist, neighbor, radii):
    """ cutting up neighbor_list
    Either A or B must be 0
    :param nei_list: is [[1,2],[0,2],[0,1]
    :param nei_dist: is [[1,2],[1,2],[1,2]]
    :param neighbor: is target number o_f neighbor atoms
    :param radii: is target distance o_f neighbor atoms
    :return [neighbor_list, neighbor_distance]: is cut up neighbor_list
    """
    new_list = [[] for i in range(len(nei_list))]
    new_dist = [[] for i in range(len(nei_list))]

    if neighbor != 0 and radii != 0:
        print("# error in mod neighbor list")
        return []

    if neighbor != 0:
        for i, _ in enumerate(nei_list):
            if len(nei_list[i]) < neighbor:
                print('# radius too small. you require ', neighbor,
                      ' neighbors. But there is only', len(nei_list[i]), 'neighbors.')
                raise SmallRadiusError()
            for j in range(neighbor):
                new_list[i].append(nei_list[i][j])
                new_dist[i].append(nei_dist[i][j])
    elif radii != 0:
        for i, _ in enumerate(nei_list):
            for j in range(len(nei_list[i])):
                dist = nei_dist[i][j]
                if dist <= radii:
                    new_list[i].append(nei_list[i][j])
                    new_dist[i].append(nei_dist[i][j])

    return [new_list, new_dist]


def add_mirror_image(orig_coord, sim_box):
    coord = [orig_coord[i] for i in range(len(orig_coord))]

    inum = [[ix, iy, iz]
            for ix in range(-1, 2) for iy in range(-1, 2) for iz in range(-1, 2)]
    inum.remove([0, 0, 0])

    for ixyz in inum:
        for i in range(len(orig_coord)):
            coord.append(
                [sim_box[0]*ixyz[0] + orig_coord[i][0],
                 sim_box[1]*ixyz[1] + orig_coord[i][1],
                 sim_box[2]*ixyz[2] + orig_coord[i][2]])
    return coord


def poly_area(poly):
    # area of polygon poly
    if len(poly) < 3:  # not a plane - no area
        return 0
    total = [0, 0, 0]
    N = len(poly)
    for i in range(N):
        vi1 = poly[i]
        vi2 = poly[(i+1) % N]
        prod = np.cross(vi1, vi2)
        total[0] += prod[0]
        total[1] += prod[1]
        total[2] += prod[2]
    result = np.dot(total, unit_normal(poly[0], poly[1], poly[2]))
    return abs(result/2)


def unit_normal(a, b, c):
    # unit normal vector of plane defined by points a, b, and c
    x = np.linalg.det([[1, a[1], a[2]],
                       [1, b[1], b[2]],
                       [1, c[1], c[2]]])
    y = np.linalg.det([[a[0], 1, a[2]],
                       [b[0], 1, b[2]],
                       [c[0], 1, c[2]]])
    z = np.linalg.det([[a[0], a[1], 1],
                       [b[0], b[1], 1],
                       [c[0], c[1], 1]])
    magnitude = (x**2 + y**2 + z**2)**.5
    return (x/magnitude, y/magnitude, z/magnitude)


def build_neighbor_delaunay(orig_coord, sim_box, settings):
    n_part = len(orig_coord)

    coord = add_mirror_image(orig_coord, sim_box)
    vor = Voronoi(coord, furthest_site=False,
                  incremental=False, qhull_options="Fv")

    neighbor_list = [[] for i in range(n_part)]
    for pair, pair_index in zip(vor.points[vor.ridge_points], vor.ridge_points):
        if min(pair_index) < n_part:
            part1 = pair_index[0]
            part2 = pair_index[1]
            if part1 < n_part:
                neighbor_list[part1].append(part2)
            if part2 < n_part:
                neighbor_list[part2].append(part1)

    surface_list = [[] for i in range(n_part)]
    for i in range(n_part):
        now_nei = neighbor_list[i]
        for j in now_nei:
            if (i, j) in vor.ridge_dict:
                facet = vor.ridge_dict[i, j]
            if (j, i) in vor.ridge_dict:
                facet = vor.ridge_dict[j, i]
            area_points = []
            for k in facet:
                area_points.append(vor.vertices[k])
            surface_area = poly_area(area_points)
            surface_list[i].append(surface_area)

    neighbor_dist = [[] for i in range(n_part)]
    nei_area = [[] for i in range(n_part)]
    for i in range(len(neighbor_list)):
        import copy
        nei_list = copy.deepcopy(neighbor_list[i])
        nei_dist = []
        nei_area_temp = {}
        for j in nei_list:
            # calc dist
            i2 = i % n_part
            j2 = j % n_part
            delta = [orig_coord[i2][k] - orig_coord[j2][k] for k in range(3)]
            for k in range(3):
                if abs(delta[k]) > sim_box[k]/2:
                    delta[k] = abs(delta[k]) - sim_box[k]
            dist = np.linalg.norm(delta)
            nei_dist.append(dist)

            # calc area
            if (i, j) in vor.ridge_dict:
                facet = vor.ridge_dict[i, j]
            if (j, i) in vor.ridge_dict:
                facet = vor.ridge_dict[j, i]
            area_points = []
            for k in facet:
                area_points.append(vor.vertices[k])
            area = poly_area(area_points)
            nei_area_temp[j] = area

        [nei_list, nei_dist] = misc.sort_by_distance([nei_list], [nei_dist])
        nei_area[i] = [nei_area_temp[j] for j in nei_list[0]]

        neighbor_list[i] = nei_list[0]
        neighbor_dist[i] = nei_dist[0]

    for i in range(len(neighbor_list)):
        for j in range(len(neighbor_list[i])):
            neighbor_list[i][j] = neighbor_list[i][j] % n_part

    return [neighbor_list, neighbor_dist, nei_area]


def build_neighbor_wrapper(coord, box_length, op_settings, thread_num):
    # calc initial thresh distance
    if 'neighbor' not in op_settings \
            and 'radius' not in op_settings \
            and 'Delaunay' not in op_settings:
        print("set neighborhood param like 'neighbor' or radius' or 'Delaunay'")
    if 'neighbor' not in op_settings:
        op_settings['neighbor'] = []
    if 'radius' not in op_settings:
        op_settings['radius'] = []

    # neighbor or radius based neighbor list build
    if op_settings['neighbor'] != [] or op_settings['radius'] != []:
        dist = 0.0
        if op_settings['neighbor'] != []:
            safe_factor = 1.7
            dist = calc_thresh(
                box_length, len(coord), max(op_settings['neighbor']), safe_factor)
        if 'radius' not in op_settings:
            op_settings['radius'] = []
        dist = max(op_settings['radius'] + [dist])

        # calc initial neighbor list
        [nei_list, nei_dist] = build_neighbor_list(
            coord, box_length, {'mode': 'thresh', 'dist': dist}, thread_num)

        # cut up neighbor_list for small radius or num of neighbor.
        neighbors = {}
        for i in op_settings['neighbor']:
            done = False
            while done is False:
                try:
                    neighbors['N' + str(i)] = mod_neighbor_list(
                        nei_list, nei_dist, i, 0)
                except SmallRadiusError:
                    # cutting up failed
                    dist = safe_factor * dist
                    [nei_list, nei_dist] = build_neighbor_list(
                        coord, box_length,
                        {'mode': 'thresh', 'dist': dist}, thread_num)
                else:
                    done = True

        for i in op_settings['radius']:
            name = ('%03.2f' % i)
            neighbors['R' + name] = mod_neighbor_list(
                nei_list, nei_dist, 0, i)

    if 'Delaunay' in op_settings:
        if op_settings['neighbor'] == [] and op_settings['radius'] == []:
            neighbors = {}
        for i in op_settings['Delaunay']:
            if i == 'standard':
                [nei_list, nei_dist, nei_area] = build_neighbor_delaunay(
                    coord, box_length, thread_num)
                neighbors['Delaunay'] = [nei_list, nei_dist, nei_area]

    return neighbors
