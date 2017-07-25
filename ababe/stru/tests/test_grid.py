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

        hnfs = HermiteLattice.HNFs_from_n_dups(self.bcc_base, 5)
        self.assertEqual(len(hnfs), 31)

        hnfs = HermiteLattice.HNFs_from_n_dups(self.bcc_base, 6)
        self.assertEqual(len(hnfs), 91)

    def test_eq(self):
        hnfs = HermiteLattice.HNFs_from_n_dups(self.bcc_base, 2)
        hnf00 = hnfs[0]
        hnf01 = hnfs[1]
        self.assertEqual(hnf00, hnf01)

        hnfs = HermiteLattice.HNFs_from_n_dups(self.bcc_base, 7)
        hnf00 = hnfs[5]
        hnf01 = hnfs[6]
        # self.assertEqual(hnf00, hnf01)

    def test_HNFs_from_n(self):
        nodup_hnfs = HermiteLattice.HNFs_from_n(self.bcc_base, 2)
        self.assertEqual(len(nodup_hnfs), 2)

        nodup_hnfs = HermiteLattice.HNFs_from_n(self.bcc_base, 3)
        self.assertEqual(len(nodup_hnfs), 3)

        nodup_hnfs = HermiteLattice.HNFs_from_n(self.bcc_base, 4)
        self.assertEqual(len(nodup_hnfs), 7)

        nodup_hnfs = HermiteLattice.HNFs_from_n(self.bcc_base, 9)
        self.assertEqual(len(nodup_hnfs), 14)

        nodup_hnfs = HermiteLattice.HNFs_from_n(self.bcc_base, 7)
        self.assertEqual(len(nodup_hnfs), 7)
        # self.assertTrue(nodup_hnfs[5].is_eq(nodup_hnfs[5], nodup_hnfs[6]))


if __name__ == "__main__":
    import nose2
    nose2.main()
