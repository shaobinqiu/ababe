# coding: utf-8
# Distributed under the terms of the MIT License.

import sys
import os.path

from ababe.stru.scaffold import SitesGrid, CStru
from ababe.stru.element import GhostSpecie, Specie
from itertools import combinations
from progressbar import ProgressBar

import numpy as np
from spglib import get_symmetry
import os

# Filename sogen is for Site-Occupy-GENerator

def is_stru_equal(struA, struB, ops):
    bA, posA, atom_numA = struA.get_cell()
    bB, posB, atom_numB = struB.get_cell()
    id_struA = _get_id_seq(posA, atom_numA)

    is_equal = False
    for r, t in ops:
        pos_new = np.transpose(r @ np.transpose(posB)) + t
        id_stru = _get_id_seq(pos_new, atom_numB)
        if id_stru == id_struA:
            is_equal = True

    return is_equal

def _get_id_seq(pos, arr_num):

    # from fractions import Fraction
    # transfer the atom position into >=0 and <=1
    pos = np.around(pos, decimals=10)
    func_tofrac = np.vectorize(lambda x: round((x % 1), 3))
    o_pos = func_tofrac(pos)
    # round_o_pos = np.around(o_pos, decimals=3)
    # z, y, x = round_o_pos[:, 2], round_o_pos[:, 1], round_o_pos[:, 0]
    z, y, x = o_pos[:, 2], o_pos[:, 1], o_pos[:, 0]
    ind_sort = np.lexsort((z, y, x))
    id_seq = str(arr_num[ind_sort])

    return id_seq

def _update_isoset(isoset, cstru, ops):
    b, pos, atom_num = cstru.get_cell()

    isoset_cstru = set()
    for r, t in ops:
        pos_new = np.transpose(r @ np.transpose(pos)) + t
        id_stru = _get_id_seq(pos_new, atom_num)
        isoset_cstru.add(id_stru)
        isoset.update(isoset_cstru)

    return isoset

def gen_nodup_cstru(lattice, sea_ele, size, speckle, num):
    d, w, l = size
    ele_sea = SitesGrid.sea(d, w, l, sea_ele)
    cell_mother_stru = CStru(lattice, ele_sea).get_cell()
    sym = get_symmetry(cell_mother_stru, symprec=1e-3)
    ops = [(r, t) for r, t in zip(sym['rotations'], sym['translations'])]
    # print(size)
    # print(lattice)

    gen_dup_cstrus = CStru.gen_speckle(lattice, sea_ele, size, speckle, num)
    isoset = set()

    # Add the progress bar when looping
    from scipy.special import comb
    number_of_structures = comb((d*w*l), num)
    bar = ProgressBar(max_value=number_of_structures)

    for cstru in bar(gen_dup_cstrus):
        b, pos, atom_num = cstru.get_cell()
        id_cstru = _get_id_seq(pos, atom_num)
        if id_cstru not in isoset:
            # print(len(ops))
            # print(len(isoset))
            # print(cstru.get_array())
            yield cstru
            _update_isoset(isoset, cstru, ops)

def default(str):
    return str + '  [Default: %(default)s]'

def lat_dict(lattice):
    from math import sqrt
    lat = { 'bcc': [[-0.5, -0.5, -0.5],
                [-0.5,  0.5,  0.5],
                [ 0.5, -0.5,  0.5]],
            'fcc': [[0, 0.5, 0.5],
                    [0.5, 0, 0.5],
                    [0.5, 0.5, 0]],
            'scc': [[1, 0, 0],
                    [0, 1, 0],
                    [0, 0, 1]],
            'triflat': [[0, 0, 20],
                        [1, 0, 0],
                        [0.5, sqrt(3)/2, 0]]
            }

    return lat[lattice]

# This function is used for remove the structures conflict with 
# the defined restricted condition
# input: a generator to produce structures
# output: a generator of structures satisfied with the restricted 
# condition.
def is_speckle_disjunct(cstru, speckle):
    m = cstru.m
    sites_arr = cstru.get_array()
    ele = speckle.Z

    pool_sites_arr = _pool_sites(sites_arr)
    ele_index = np.argwhere(pool_sites_arr==ele)
    points = np.array([_index2coor(ind, m) for ind in ele_index])
    min_d = _min_dist(points)
    is_disjunct = min_d > 1.01

    return is_disjunct

def _min_dist(points):
    # get the closest pair of points
    # Brute-force algorithm
    min_distance = 9999
    pairs = combinations(points, 2)
    for pair in pairs:
        if _dist(pair[0], pair[1]) < min_distance:
            min_distance = _dist(pair[0], pair[1])

    return min_distance

def _dist(p,q):
    dist = np.linalg.norm(p-q)
    return dist

def _pool_sites(sites_arr):
    d, w, l = np.shape(sites_arr)
    pool = sites_arr    
    # pool the elements of outer dimension (depth)
    depth_d = pool[0, :, :].reshape(1,w,l)
    pool = np.concatenate((pool, depth_d), axis=0)
    # pool the elements of meddle dimension (width)
    width_d = pool[:, 0, :].reshape(d+1, 1, l)
    pool = np.concatenate((pool, width_d), axis=1)
    # pool the elements of inner dimension (length)
    length_d = pool[:, :, 0].reshape(d+1, w+1, 1)
    pool = np.concatenate((pool, length_d), axis=2)

    return pool

def _index2coor(ind, m):
    m_arr = np.array(m)
    d, w, l = ind
    v1 = m_arr[0]*d
    v2 = m_arr[1]*w
    v3 = m_arr[2]*l
    cood = np.array([v1[0]+v2[0]+v3[0], v1[1]+v2[1]+v3[1], v1[2]+v2[2]+v3[2]])
    return cood

# def main():
    # parser = argparse.ArgumentParser()
    # parser.add_argument('--lattice', choices=['bcc', 'fcc', 'scc', 'triflat'],
    #                         help='Lattice type of grid conventional cell')
    # parser.add_argument('-b', '--base', dest='sea', required=True,
    #                         help='Element abbreviation of the base specie')
    # parser.add_argument('-g', '--size', nargs=3, dest='size', required=True,
    #                         help='Grid size of structure', type=int)
    # parser.add_argument('-s', '--speckle', dest='speckle', required=True,
    #                         help='Element abbreviation of the speckle specie')
    # parser.add_argument('-n', '--num', dest='number', type=int, 
    #                         help=default('Number of speckles filled in the base'), default=2)
    # parser.add_argument('-o', '--output-type', 
    #                         help=default('Output type of generated non-duplicate periodic grid structure'), 
    #                             default='normal')

    # args = parser.parse_args()
    # size = args.size
    # sea_ele = Specie(args.sea)
    # speckle = Specie(args.speckle)

    # nodup_gen = gen_nodup_cstru(lat_dict(args.lattice), sea_ele, size, speckle, args.number)
    # with open('allstru.txt', 'w') as f:
    #     for s in nodup_gen:
    #         basis, pos, atom = s.get_cell()
    #         f.write('ONE NEW STRUCTURE:\n')
    #         f.write('The basis is:\n')
    #         f.write('\n'.join(str(line) for line in basis))

    #         f.write('\nThe position is:\n')
    #         f.write('\n'.join(str(line) for line in pos))

    #         f.write('\nThe elements is:\n')
    #         f.write(str(atom))

    #         f.write('\n\n\n')