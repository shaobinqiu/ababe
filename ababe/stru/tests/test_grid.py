# coding: utf-8
# Distributed under the terms of the MIT License.
#
import unittest
import numpy as np

from ababe.stru.grid import HermiteLattice


class testHermiteLattice(unittest.TestCase):

    def setUp(self):
        self.bcc_base = np.array([[-0.5, -0.5, -0.5],
                                  [-0.5,  0.5,  0.5],
                                  [0.5, -0.5,  0.5]])

    def test_HNFs_from_n_dups(self):
        hnfs = HermiteLattice.HNFs_from_n_dups(self.bcc_base, 4)
        self.assertEqual(len(hnfs), 35)


if __name__ == "__main__":
    import nose2
    nose2.main()
