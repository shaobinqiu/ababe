#!/usr/bin/env python
import argparse
import sys
import os.path

sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from ababe.stru.scaffold import SitesGrid, CStru
from ababe.stru.element import GhostSpecie, Specie

import numpy as np
from spglib import get_symmetry
import os

def _get_id_seq(pos, arr_num):
    func_tofrac = np.vectorize(lambda x: x % 1)
    o_pos = func_tofrac(pos)
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
    sym = get_symmetry(cell_mother_stru, symprec=1e-5)
    ops = [(r, t) for r, t in zip(sym['rotations'], sym['translations'])]

    gen_dup_cstrus = CStru.gen_speckle(lattice, sea_ele, size, speckle, num)
    isoset = set()
    for cstru in gen_dup_cstrus:
        b, pos, atom_num = cstru.get_cell()
        id_cstru = _get_id_seq(pos, atom_num)
        if id_cstru not in isoset:
            _update_isoset(isoset, cstru, ops)
            yield cstru


def default(str):
    return str + '  [Default: %(default)s]'

def lat_dict(lattice):
    lat = { 'bcc': [[-0.5, -0.5, -0.5],
                [-0.5,  0.5,  0.5],
                [ 0.5, -0.5,  0.5]],
            'fcc': [[0, 0.5, 0.5],
                    [0.5, 0, 0.5],
                    [0.5, 0.5, 0]],
            'scc': [[1, 0, 0],
                    [0, 1, 0],
                    [0, 0, 1]]}

    return lat[lattice]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--lattice', choices=['bcc', 'fcc', 'scc'],
                            help='Lattice type of grid conventional cell')
    parser.add_argument('-b', '--base', dest='sea', required=True,
                            help='Element abbreviation of the base specie')
    parser.add_argument('-g', '--size', nargs=3, dest='size', required=True,
                            help='Grid size of structure', type=int)
    parser.add_argument('-s', '--speckle', dest='speckle', required=True,
                            help='Element abbreviation of the speckle specie')
    parser.add_argument('-n', '--num', dest='number', type=int, 
                            help=default('Number of speckles filled in the base'), default=2)
    parser.add_argument('-o', '--output-type', 
                            help=default('Output type of generated non-duplicate periodic grid structure'), 
                                default='normal')

    args = parser.parse_args()
    size = args.size
    sea_ele = Specie(args.sea)
    speckle = Specie(args.speckle)

    nodup_gen = gen_nodup_cstru(lat_dict(args.lattice), sea_ele, size, speckle, args.number)
    with open('allstru.txt', 'w') as f:
        for s in nodup_gen:
            basis, pos, atom = s.get_cell()
            f.write('ONE NEW STRUCTURE:\n')
            f.write('The basis is:\n')
            f.write('\n'.join(str(line) for line in basis))

            f.write('\nThe position is:\n')
            f.write('\n'.join(str(line) for line in pos))

            f.write('\nThe elements is:\n')
            f.write(str(atom))

            f.write('\n\n\n')
    # print(args.lattice)
    # print(args.sea)
    # print(args.size)
    # print(args.speckle)
    # print(args.number)


if __name__ == "__main__":
    main()