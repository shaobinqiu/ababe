# coding: utf-8
# Distributed under the terms of the MIT License.

import itertools
import numpy as np
from functools import reduce

# import pdb


class HermiteLattice(object):
    """
    The class will produce the instance which is a Hermite Normal
    Form of a superlattice. It can be used to generate a GeneralCell.
    """

    def __init__(self, unit_bases, lat_coeff):
        pass

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
                        l_HNFs.append(hnf)

        return l_HNFs
