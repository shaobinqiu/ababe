# coding: utf-8
# Distributed under the terms of the MIT License.

import numpy as np
# import collections

from ababe.stru.element import Specie, GhostSpecie
from itertools import combinations

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
    def sea(cls, depth, width, length, sp = GhostSpecie()):
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
        if other == None: return False
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
        rarr = (sp.Z - bsp.Z)*np.random.randint(2, size = size)
        sarr = np.zeros(size, dtype = np.int)+bsp.Z
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
            arr = np.array(out, dtype = np.int).reshape(size)
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
        if other == None: return False
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
        marr = np.array(self._matrix, dtype = np.float64).reshape((3,3))
        g_arr = self._sites_grid.to_array()
        d = self.depth
        w = self.width
        l = self.length

        arr_bas = marr*np.array([d,w,l], dtype = np.int).reshape((3,1))
        grid_position = np.array([p for p in CStru._yield_position(d, w, l)]) 
        frac = np.array([1/d, 1/w, 1/l], dtype = np.float64).reshape((1,3))
        arr_pos = grid_position * frac
        arr_num = np.array([i for i in g_arr.flat])

        return (arr_bas, arr_pos, arr_num)
