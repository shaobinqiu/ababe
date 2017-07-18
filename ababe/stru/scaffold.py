# coding: utf-8
# Distributed under the terms of the MIT License.
from __future__ import division

import numpy as np
# import collections

from ababe.stru.element import Specie, GhostSpecie
from itertools import combinations

from scipy.spatial import cKDTree
from operator import itemgetter
import spglib
import xxhash


class SitesGrid(object):
    """
    Grid object. Used for constructed grids where to put the atoms on.
    Like a chess board.
    """

    def __init__(self, sites):
        self._sites = sites
        self._depth = len(sites)
        self._width = len(sites[0])
        self._length = len(sites[0][0])

    @classmethod
    def sea(cls, depth, width, length, sp=GhostSpecie()):
        sites = [[[sp for _ in range(length)]
                          for _ in range(width)]
                              for _ in range(depth)]

        return cls(sites)

    @property
    def sites(self):
        return self._sites

    @property
    def depth(self):
        return self._depth

    @property
    def width(self):
        return self._width

    @property
    def length(self):
        return self._length

    def __getitem__(self, pos):
        d, w, l = pos
        return self._sites[d][w][l]

    def __setitem__(self, pos, sp):
        d, w, l = pos
        self._sites[d][w][l] = sp

    def __eq__(self, other):
        if other is None:
            return False
        return self._sites == other._sites

    def deepCopy(self):
        g = SitesGrid(self._sites)
        g._sites = [x[:][:] for x in self._sites]
        return g

    def to_array(self):
        mfunc = np.vectorize(lambda sp: sp.Z)
        arr = mfunc(np.array(self._sites))
        return arr

    @classmethod
    def from_array(cls, arr):
        mfunc = np.vectorize(lambda n: Specie.to_sp(n))
        sarr = mfunc(arr)
        return cls(sarr.tolist())

    @classmethod
    def random_fill(cls, bsp, size, sp):
        # d, w, l = size
        rarr = (sp.Z - bsp.Z)*np.random.randint(2, size=size)
        sarr = np.zeros(size, dtype=np.int)+bsp.Z
        arr = sarr + rarr
        return cls.from_array(arr)

    @classmethod
    def gen_speckle(cls, ssp, size, sp, noa):
        d, w, l = size
        n = d * w * l
        i_sea = ssp.Z
        i_speckle = sp.Z
        for w_on in combinations(range(n), noa):
            out = [i_sea]*n
            for index in w_on:
                out[index] = i_speckle
            arr = np.array(out, dtype=np.int).reshape(size)
            yield cls.from_array(arr)


class CStru(object):

    def __init__(self, m, sg):
        self._matrix = m
        self._sites_grid = sg
        self.depth = sg.depth
        self.width = sg.width
        self.length = sg.length

    @property
    def m(self):
        return self._matrix

    @property
    def sites_grid(self):
        return self._sites_grid

    # @property
    # def depth(self):
    #     return self.sites_grid.depth

    # @property
    # def width(self):
    #     return self.sites_grid.width

    # @property
    # def length(self):
    #     return self.sites_grid.length

    # def get_grid(self):
    #     return self._sites_grid.sites

    def get_array(self):
        return self._sites_grid.to_array()

    def __eq__(self, other):
        if other is None:
            return False
        return other.m == self.m and other.sites_grid == self.sites_grid

    @classmethod
    def from_array(cls, m, arr):
        return cls(m, SitesGrid.from_array(arr))

    @classmethod
    def gen_speckle(cls, m, ssp, size, sp, noa):
        for stru in SitesGrid.gen_speckle(ssp, size, sp, noa):
            yield cls(m, stru)

    @staticmethod
    def _yield_position(d, w, l):
        for c in range(d):
            for b in range(w):
                for a in range(l):
                    yield [c, b, a]

    def get_cell(self):

        # from fractions import Fraction

        marr = np.array(self._matrix, dtype=np.float64).reshape((3, 3))
        g_arr = self._sites_grid.to_array()
        d = self.depth
        w = self.width
        l = self.length

        arr_bas = marr*np.array([d, w, l], dtype=np.int).reshape((3, 1))
        grid_position = np.array([p for p in CStru._yield_position(d, w, l)])
        frac = np.array([1/d, 1/w, 1/l], dtype=np.float64).reshape((1, 3))
        # round_frac = np.around(frac, decimals=22)
        arr_pos = grid_position * frac
        arr_num = np.array([i for i in g_arr.flat])

        return (arr_bas, arr_pos, arr_num)

    def get_lattice(self):
        arr_bas, arr_pos, arr_num = self.get_cell()
        return arr_bas

    def get_positions(self):
        arr_bas, arr_pos, arr_num = self.get_cell()
        return arr_pos

    def get_atoms(self):
        arr_bas, arr_pos, arr_num = self.get_cell()
        return arr_num

    @staticmethod
    def get_id_matrix(cell, d, w, l):
        arr_num = cell[2]

        return arr_num.reshape((d, w, l))

    def get_midpoint(self):
        d = self.depth
        w = self.width
        l = self.length
        return (d//2, w//2, l//2)

    # @staticmethod
    # def _pos2coor(pos):
    #     a, b = np.array(self.m)
    #     x, y = pos
    #     coor = a*x + b*y    # an array
    #     return tuple(coor)

    def get_neighbors(self, pos, delta):

        def _pos2coor(pos):
            a, b, c = np.array(self.m)
            x, y, z = pos
            coor = a*x + b*y + c*z    # an array
            return tuple(coor)

        def p_gen():
            for z in range(self.depth):
                for x in range(self.width):
                    for y in range(self.length):
                        yield(x, y, z)

        point = _pos2coor(pos)
        # w = self.width
        # l = self.length
        coor_map = {p: _pos2coor(p) for p in p_gen()}
        del coor_map[pos]

        points = list(coor_map.values())
        points_tree = cKDTree(points)
        ind = points_tree.query_ball_point(point, delta)
        neighbors = itemgetter(*ind)(list(coor_map.keys()))
        return set(neighbors)


class GeneralCell(object):
    """
    A Cell data structure used for generate all nonduplicated structure.
    Initialized by three np.array
    """
    def __init__(self, lattice, positions, numbers):
        self._lattice = lattice
        init_index = self._get_new_id_seq(positions, numbers)
        self._positions = positions[init_index]
        self._numbers = numbers
        self._spg_cell = (self._lattice, self._positions, self._numbers)
        self._num_count = numbers.size

    def get_speckle_num(self, sp):
        from collections import Counter
        num = Counter(self.numbers)[sp.Z]
        # num = num_count[atom]
        return num

    @staticmethod
    def _get_new_id_seq(pos, numbers):
        """
        A helper function to produce the new sequence of the transformed
        structure. Algs is sort the position back to init and use the index
        to sort numbers.
        """
        # transfer the atom position into >=0 and <=1
        pos = np.around(pos, decimals=3)
        func_tofrac = np.vectorize(lambda x: round((x % 1), 3))
        o_pos = func_tofrac(pos)
        # round_o_pos = np.around(o_pos, decimals=3)
        # z, y, x = round_o_pos[:, 2], round_o_pos[:, 1], round_o_pos[:, 0]
        z, y, x = o_pos[:, 2], o_pos[:, 1], o_pos[:, 0]
        inds = np.lexsort((z, y, x))

        return inds

    @property
    def spg_cell(self):
        return self._spg_cell

    @property
    def lattice(self):
        return self._lattice

    @property
    def positions(self):
        return self._positions

    @property
    def numbers(self):
        return self._numbers

    @numbers.setter
    def numbers(self, arr_numbers):
        self._numbers = arr_numbers

    @property
    def num_count(self):
        """
        number of atoms
        """
        return self._num_count

    @property
    def id(self):
        num_id = xxhash.xxh64(self.numbers).intdigest()
        return num_id

    def get_spacegroup(self):
        return spglib.get_spacegroup(self._spg_cell, symprec=1e-4)

    def get_symmetry(self):
        """
        Symmetry operations are obtained as a dictionary.
        The key rotation contains a numpy array of integer,
        which is “number of symmetry operations” x “3x3 matrices”.
        The key translation contains a numpy array of float,
        which is “number of symmetry operations” x “vectors”.
        """
        symmetry = spglib.get_symmetry(self._spg_cell, symprec=1e-4)
        return symmetry

    def get_symmetry_permutation(self):
        """
        This a object function to get the permutation group operators.
        Represented as a table.
        """
        sym_perm = []
        numbers = [i for i in range(self.num_count)]
        sym_mat = spglib.get_symmetry(self._spg_cell, symprec=1e-4)
        ops = [(r, t) for r, t in zip(sym_mat['rotations'], sym_mat['translations'])]
        for r, t in ops:
            pos_new = np.transpose(np.matmul(r, np.transpose(self._positions))) + t
            perm = self._get_new_id_seq(pos_new, numbers)
            sym_perm.append(perm)

        return sym_perm

