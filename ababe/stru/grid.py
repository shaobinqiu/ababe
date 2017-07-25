# coding: utf-8
# Distributed under the terms of the MIT License.

import itertools
import numpy as np
import spglib
from functools import reduce

# import pdb


class HermiteLattice(object):
    """
    The class will produce the instance which is a Hermite Normal
    Form of a superlattice. It can be used to generate a GeneralCell.
    """

    def __init__(self, unit_bases, lat_coeff):
        self.ub = unit_bases
        self.lat_coeff = lat_coeff
        cell = (self.ub, np.array([[0, 0, 0]]), np.array([0]))
        self.sym = spglib.get_symmetry(cell)

    @classmethod
    def HNFs_from_n_dups(cls, unit_bases, n):
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
                        hnf = np.array([[a, 0, 0],
                                        [b, c, 0],
                                        [d, e, f]])
                        l_HNFs.append(cls(unit_bases, hnf))

        return l_HNFs

    def __eq__(self, other):
        inv = np.linalg.inv
        mul = np.matmul
        for r in self.sym['rotations']:
            h_inv = mul(inv(other.lat_coeff),
                        inv(r))
            # h = mul(r, other.lat_coeff)
            h_mat = mul(h_inv, self.lat_coeff)
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
    def HNFs_from_n(cls, unit_bases, n):
        hnfs = cls.HNFs_from_n_dups(unit_bases, n)
        nodup_hnfs = []
        for hnf in hnfs:
            if hnf not in nodup_hnfs:
                nodup_hnfs.append(hnf)

        return nodup_hnfs

    def to_general_cell(self):
        pass
