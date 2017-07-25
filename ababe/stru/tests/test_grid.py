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
        self.bcc_u_position = np.array([[0, 0, 0]])
        self.bcc_u_n = np.array([0])
        self.bcc_uc = (self.bcc_base,
                       self.bcc_u_position,
                       self.bcc_u_n)

    def test_HNFs_from_n_dups(self):
        hnfs = HermiteLattice.HNFs_from_n_dups(self.bcc_uc, 4)
        self.assertEqual(len(hnfs), 35)

        hnfs = HermiteLattice.HNFs_from_n_dups(self.bcc_uc, 5)
        self.assertEqual(len(hnfs), 31)

        hnfs = HermiteLattice.HNFs_from_n_dups(self.bcc_uc, 6)
        self.assertEqual(len(hnfs), 91)

    def test_eq(self):
        hnfs = HermiteLattice.HNFs_from_n_dups(self.bcc_uc, 2)
        hnf00 = hnfs[0]
        hnf01 = hnfs[1]
        self.assertEqual(hnf00, hnf01)

    def test_HNFs_from_n(self):
        # use bcc data from <PHYSICAL REVIEW B 80, 014120 (2009)>
        # to test...
        results = [2, 3, 7, 5, 10, 7]
        for i, result in zip(range(2, 8), results):
            nodup_hnfs = HermiteLattice.HNFs_from_n(self.bcc_uc, i)
            self.assertEqual(len(nodup_hnfs), result)

        # hcp test
        hcp_b = np.array([[2.51900005,  0.,  0.],
                          [-1.25950003,  2.18151804, 0.],
                          [0., 0.,  4.09100008]])
        hcp_positions = np.array([[0.33333334,  0.66666669,  0.25],
                                  [0.66666663,  0.33333331,  0.75]])
        hcp_numbers = np.array([0, 0])
        hcp_uc = (hcp_b, hcp_positions, hcp_numbers)
        result = HermiteLattice.HNFs_from_n(hcp_uc, 9)
        self.assertEqual(len(result), 23)


if __name__ == "__main__":
    import nose2
    nose2.main()
