# coding: utf-8
# Distributed under the terms of the MIT License.
#
import unittest
import numpy as np

from ababe.stru.grid import SuperLatticeGenerator


class testSuperLatticeGenerator(unittest.TestCase):

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
        hnfs = SuperLatticeGenerator.hnfs_from_n_dups(self.bcc_uc, 4)
        self.assertEqual(len(hnfs), 35)

        hnfs = SuperLatticeGenerator.hnfs_from_n_dups(self.bcc_uc, 5)
        self.assertEqual(len(hnfs), 31)

        hnfs = SuperLatticeGenerator.hnfs_from_n_dups(self.bcc_uc, 6)
        self.assertEqual(len(hnfs), 91)

    def test_eq(self):
        hnfs = SuperLatticeGenerator.hnfs_from_n_dups(self.bcc_uc, 2)
        hnf00 = hnfs[0]
        hnf01 = hnfs[1]
        self.assertEqual(hnf00, hnf01)

    def test_HNFs_from_n(self):
        # use bcc data from <PHYSICAL REVIEW B 80, 014120 (2009)>
        # to test...
        results = [2, 3, 7, 5, 10, 7]
        for i, result in zip(range(2, 8), results):
            nodup_hnfs = SuperLatticeGenerator.hnfs_from_n(self.bcc_uc, i)
            self.assertEqual(len(nodup_hnfs), result)

        # hcp test
        hcp_b = np.array([[2.51900005,  0.,  0.],
                          [-1.25950003,  2.18151804, 0.],
                          [0., 0.,  4.09100008]])
        hcp_positions = np.array([[0.33333334,  0.66666669,  0.25],
                                  [0.66666663,  0.33333331,  0.75]])
        hcp_numbers = np.array([0, 0])
        hcp_uc = (hcp_b, hcp_positions, hcp_numbers)
        result = SuperLatticeGenerator.hnfs_from_n(hcp_uc, 9)
        self.assertEqual(len(result), 23)

    def test_to_general_cell(self):
        hnfs = SuperLatticeGenerator.hnfs_from_n_dups(self.bcc_uc, 4)
        hnf = hnfs[2]
        cell = hnf.to_general_cell()
        # print(cell.spg_cell)
        self.assertEqual(len(cell.spg_cell[2]), 4)

        zb_b = np.array([[3.82863, 0., 0.],
                         [1.91431, 3.31569, 0.],
                         [1.91431, 1.10523, 3.12606]])
        zb_pos = np.array([[0., 0., 0.],
                           [0.25, 0.25, 0.25]])
        zb_num = np.array([30, 16])
        zb_uc = (zb_b, zb_pos, zb_num)
        zbs = SuperLatticeGenerator.hnfs_from_n(zb_uc, 3)
        one_zb = zbs[1]
        cell = one_zb.to_general_cell()
        # print(cell.spg_cell)
        self.assertEqual(len(cell.spg_cell[2]), 6)


if __name__ == "__main__":
    import nose2
    nose2.main()
