#!/usr/bin/env python
import argparse
from ababe.stru.scaffold import SitesGrid, CStru

import numpy as np
from spglib import get_symmetry

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

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--lattice', choices=['bcc', 'fcc', 'scc'],
                            help='Lattice type of grid conventional cell')
    parser.add_argument('-b', '--base', dest='sea', required=True,
                            help='Element abbreviation of the base specie')
    parser.add_argument('-g', '--size', nargs=3, dest='size', required=True,
                            help='Grid size of structure')
    parser.add_argument('-s', '--speckle', dest='speckle', required=True,
                            help='Element abbreviation of the speckle specie')
    parser.add_argument('-n', '--num', dest='number', type=int, 
                            help=default('Number of speckles filled in the base'), default=2)

    args = parser.parse_args()
    # print(args.lattice)
    # print(args.sea)
    # print(args.size)
    # print(args.speckle)
    # print(args.number)


if __name__ == "__main__":
    main()