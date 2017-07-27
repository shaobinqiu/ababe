# coding: utf-8
# Distributed under the terms of the MIT License.

import itertools
import numpy as np
import spglib
from functools import reduce
from progressbar import ProgressBar
# import pdb
from itertools import product

from ababe.stru.scaffold import GeneralCell


class SuperLatticeGenerator(object):
    """
    The class will produce the instance which is a Hermite Normal
    Form of a superlattice. It can be used to generate a GeneralCell.
    TODO: input present, unit_cell is row vectors, which lat_coeff
    is column vectors. SHOULD CHNAGE code to make lat_coeff be a
    row vectors.
    """

    def __init__(self, unit_cell, lat_coeff):
        self.ub = unit_cell[0]
        self.upositions = unit_cell[1]
        self.unumbers = unit_cell[2]
        self.lat_coeff = lat_coeff
        self.unit_cell = unit_cell

        self.sym = spglib.get_symmetry(self.unit_cell)

    @classmethod
    def hnfs_from_n_dups(cls, unit_cell, n):
        def factors(n):
            return set(reduce(list.__add__,
                              ([i, n//i] for i in
                                  range(1, int(n**0.5) + 1) if n % i == 0)))

        l_HNFs = []
        a_list = list(factors(n))
        for a in a_list:
            c_list = list(factors(n//a))
            for c in c_list:
                f = n//a//c
                for b in range(c):
                    # pdb.set_trace()
                    for d, e in itertools.product(range(f), repeat=2):
                        hnf = np.array([[a, b, d],
                                        [0, c, e],
                                        [0, 0, f]])
                        l_HNFs.append(cls(unit_cell, hnf))

        return l_HNFs

    def __eq__(self, other):
        # H_j * R.T ^-1 * H ^-1 should be an int matrix
        inv = np.linalg.inv
        mul = np.matmul
        for r in self.sym['rotations']:
            h_inv = mul(other.lat_coeff,
                        inv(r.T))
            # h = mul(r, other.lat_coeff)
            h_mat = mul(h_inv, inv(self.lat_coeff))
            h_mat = np.around(h_mat, decimals=3)
            if np.all(np.mod(h_mat, 1) == 0):
                return True

        return False

    # def is_eq(self, my, other):
    #     inv = np.linalg.inv
    #     mul = np.matmul
    #     for r in self.sym['rotations']:
    #         h_inv = mul(inv(other.lat_coeff),
    #                     inv(r))
    #         # h = mul(r, other.lat_coeff)
    #         h_mat = mul(h_inv, my.lat_coeff)
    #         h_mat = np.around(h_mat, decimals=2)
    #         # pdb.set_trace()
    #         if np.all(np.mod(h_mat, 1) == 0):
    #             return True

    #     return False

    @classmethod
    def hnfs_from_n(cls, unit_cell, n):
        hnfs = cls.hnfs_from_n_dups(unit_cell, n)
        nodup_hnfs = []
        bar = ProgressBar()
        for hnf in bar(hnfs):
            if hnf not in nodup_hnfs:
                nodup_hnfs.append(hnf)

        # pdb.set_trace()

        return nodup_hnfs

    def to_general_cell(self):
        """
        The function used to convert the superlattice
        HermiteLattice to a GeneralCell instance.
        input aps for atome_position_s, which are atom positions
        of the unit basis.
        input numbers are element number of the corespoding positions.
        """
        # lat_coeff is represent as column vector
        # while ub and latt is row vector
        latt = np.matmul(self.lat_coeff,
                         self.ub)

        o_unit_pos = self.upositions/np.amax(self.lat_coeff)
        o_pos = self.get_frac_from_H(self.lat_coeff)
        l_of_positions = [i for i in map(lambda x: x+o_pos, list(o_unit_pos))]
        # pdb.set_trace()
        pos = np.concatenate(l_of_positions, axis=0)

        n = self.lat_coeff.diagonal().prod()
        numbers = np.repeat(self.unumbers, n)

        # pdb.set_trace()
        return GeneralCell(latt, pos, numbers)

    @staticmethod
    def get_frac_from_H(h_mat):
        inv = np.linalg.inv
        mul = np.matmul
        m = np.amax(h_mat)
        int_coor_all = np.array([i for i in product(range(m*3), repeat=3)])
        frac_all = mul(int_coor_all, inv(h_mat))
        # frac_all = mul(int_coor_all, inv(h_mat))
        # print(frac_all)
        is_incell = np.all(((frac_all >= 0) & (frac_all < 1)),
                           axis=1)
        ind = np.where(is_incell)[0]
        # pdb.set_trace()
        return frac_all[ind]
