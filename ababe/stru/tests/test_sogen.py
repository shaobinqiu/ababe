# encoding: utf-8
# Distributed under the terms of the MIT License.

import unittest

import numpy as np
from spglib import get_symmetry
import ababe.stru.sogen as sogen
from ababe.stru.sogen import OccupyGenerator
from ababe.stru.element import GhostSpecie, Specie
from ababe.stru.scaffold import SitesGrid, CStru, GeneralCell


class testOccupyGeneratorCell(unittest.TestCase):

    def setUp(self):
        self.arr_lat = np.array([[3.0, 0, 0], [0, 2.0, 0.0], [0, 0, 1.0]])
        positions = [
                        [0.00000, 0.00000, 0.00000],
                        [0.00000, 0.50000, 0.00000],
                        [0.33333, 0.00000, 0.00000],
                        [0.33333, 0.50000, 0.00000],
                        [0.66666, 0.00000, 0.00000],
                        [0.66666, 0.50000, 0.00000],
                        [0.16666, 0.25000, 0.50000],
                        [0.16666, 0.75000, 0.50000],
                        [0.50000, 0.25000, 0.50000],
                        [0.50000, 0.75000, 0.50000],
                        [0.83333, 0.25000, 0.50000],
                        [0.83333, 0.75000, 0.50000]
                    ]
        self.arr_positions = np.array(positions)
        arr_numbers_0 = np.array([6]*12)
        self.cell = GeneralCell(self.arr_lat, self.arr_positions, arr_numbers_0)
        self.ocu_gen = OccupyGenerator(self.cell)

        tmp = arr_numbers_0.copy()
        tmp[0] = 5
        arr_numbers_a = tmp

        tmp = arr_numbers_0.copy()
        tmp[1] = 5
        arr_numbers_b = tmp

        self.cell_a = GeneralCell(self.arr_lat, self.arr_positions, arr_numbers_a)
        self.cell_b = GeneralCell(self.arr_lat, self.arr_positions, arr_numbers_b)

        self.numbers_3A = np.array([5, 5, 5, 6, 6, 6, 6, 6, 6, 6, 6, 6])
        self.numbers_3B = np.array([5, 5, 6, 6, 6, 6, 6, 6, 6, 6, 5, 6])

        self.numbers_3C = np.array([5, 5, 6, 6, 5, 6, 6, 6, 6, 6, 6, 6])
        self.numbers_3D = np.array([5, 5, 6, 6, 6, 6, 6, 6, 5, 6, 6, 6])

    def test_is_equivalent(self):
        # perm_sym = self.cell.get_symmetry_permutation()
        self.assertTrue(self.ocu_gen.is_equivalent(self.cell_a, self.cell_b))

        cell_3A = GeneralCell(self.arr_lat, self.arr_positions, self.numbers_3A)
        cell_3B = GeneralCell(self.arr_lat, self.arr_positions, self.numbers_3B)
        cell_3C = GeneralCell(self.arr_lat, self.arr_positions, self.numbers_3C)
        cell_3D = GeneralCell(self.arr_lat, self.arr_positions, self.numbers_3D)

        self.assertTrue(self.ocu_gen.is_equivalent(cell_3A, cell_3B))
        self.assertTrue(self.ocu_gen.is_equivalent(cell_3C, cell_3D))


    def test_gen_dup(self):
        dup_gen = self.ocu_gen.gen_dup(3, Specie('B'))  # a generator
        l = [i for i in dup_gen]
        self.assertEqual(len(l), 220)

    def test_gen_nodup(self):
        nodup_gen = self.ocu_gen.gen_nodup(3, Specie('B'))
        l = [i for i in nodup_gen]
        self.assertEqual(len(l), 9)

        nodup_gen = self.ocu_gen.gen_nodup(4, Specie('B'))
        l = [i for i in nodup_gen]
        self.assertEqual(len(l), 21)


class testAlgorithomSog(unittest.TestCase):

    # def setUp(self):
    #     pos_01 = 

    def test_get_id_seq(self):
        pos_0 = np.array([[ 0.        ,  0.        ,  0.        ],
                           [ 0.        ,  0.        ,  0.33333333],
                           [ 0.        ,  0.        ,  0.6666666],
                           [ 0.        ,  0.5       ,  0.        ],
                           [ 0.        ,  0.5       ,  0.33333333],
                           [ 0.        ,  0.5       ,  0.66666667]])

        pos_01 = np.array([[ 0.        ,  0.        ,  0.        ],
                           [ 0.        ,  0.        ,  2/3],
                           [ 0.        ,  0.        ,  0.33333333-3],
                           [ 0.        ,  12.500003       ,  0.        ],
                           [ 0.        ,  0.5       ,  0.33333333],
                           [ 0.        ,  0.5       ,  0.66666667]])
        arr_num_01 = np.array([n for n in np.array([[[22,29,22],
                                                    [22,22,22]]]).flat])
        a_id_01 = sogen._get_id_seq(pos_01, arr_num_01)

        pos_02 = np.array([[ 0.        ,  0.        ,  0.        ],
                           [ 0.        ,  0.        ,  0.33333333],
                           [ 0.        ,  0.5       ,  0.        ],
                           [ 0.        ,  0.5       ,  0.33333333],
                           [ 0.        ,  0.        ,  0.66666667],
                           [ 0.        ,  0.5       ,  0.66666667]])
        arr_num_02 = np.array([n for n in np.array([[[22,22,22],
                                                    [22,29,22]]]).flat])
        a_id_02 = sogen._get_id_seq(pos_02, arr_num_02)

        pos_1 = pos_0.copy()
        pos_1[2][2] -= 4
        # arr_num_0 = np.array(n for n in np.array([[[22,22,22],
        #                                             [22,22,22]]]).flat)
        arr_num_00 = np.array([n for n in np.array([[[22,22,29],
                                                    [22,22,22]]]).flat])
        a_id = sogen._get_id_seq(pos_0, arr_num_00)
        s = set()
        s.add(a_id)
        s.add(a_id)
        self.assertEqual(len(s), 1)
        self.assertEqual(sogen._get_id_seq(pos_1, arr_num_00), a_id)

        self.assertEqual(a_id_01, a_id)
        self.assertEqual(a_id_02, a_id)


    def test_update_isoset(self):
        c = Specie("Cu")
        t = Specie("Ti")
        m = [[-0.5, -0.5, -0.5],
             [-0.5,  0.5,  0.5],
             [ 0.5, -0.5,  0.5]]
        ele_sea = SitesGrid.sea(2, 2, 2, c)
        cell_mother_stru = CStru(m, ele_sea).get_cell()
        sym = get_symmetry(cell_mother_stru, symprec=1e-5)
        ops = [(r, t) for r, t in zip(sym['rotations'], sym['translations'])]
        sym_perm = sogen.get_permutation_cell(cell_mother_stru)

        sites_0 = [[[c, c],
                    [c, c]],

                   [[c, c],
                    [t, c]]]
        sg_0 = SitesGrid(sites_0)
        cstru01 = CStru(m, sg_0)
        number01 = cstru01.get_cell()[2]

        isoset_init = set()
        isoset_init_copy = isoset_init.copy()
        isoset_a01 = sogen._update_isoset(isoset_init, number01, sym_perm)
        self.assertNotEqual(isoset_a01, isoset_init_copy)
        self.assertIsInstance(isoset_a01, set)

        isoset_a01_copy = isoset_a01.copy()
        isoset_a02 = sogen._update_isoset(isoset_a01, number01, sym_perm)
        self.assertEqual(isoset_a02, isoset_a01_copy)
        self.assertLessEqual(len(isoset_a01), len(ops))

    def test_gen_nodup_cstru(self):
        c = Specie("Cu")
        t = Specie("Ti")
        m = [[-0.5, -0.5, -0.5],
             [-0.5,  0.5,  0.5],
             [ 0.5, -0.5,  0.5]]
        ele_sea = SitesGrid.sea(2, 2, 2, c)
        cell_mother_stru = CStru(m, ele_sea).get_cell()
        sym = get_symmetry(cell_mother_stru, symprec=1e-3)
        ops = [(r, t) for r, t in zip(sym['rotations'], sym['translations'])]

        sites_0 = [[[c, c],
                    [c, c]],

                   [[c, c],
                    [t, c]]]
        sg_0 = SitesGrid(sites_0)
        cstru01 = CStru(m, sg_0)

        gen_01 = sogen.gen_nodup_cstru(m, c, (2,2,2), t, 1)
        nodup_01 = [stru for stru in gen_01]
        self.assertEqual(len(nodup_01), 1)

        gen_02 = sogen.gen_nodup_cstru(m, c, (1,2,8), t, 4)
        nodup_02 = [stru for stru in gen_02]
        # eq_(len(nodup_02), 51)

        m_tri = [[0, 0, 20],
                        [1, 0, 0],
                        [0.5, 0.8660254, 0]]
        ele_sea = SitesGrid.sea(1, 3, 3, c)
        cell_mother_stru = CStru(m, ele_sea).get_cell()
        sym = get_symmetry(cell_mother_stru, symprec=1e-3)
        ops = [(r, t) for r, t in zip(sym['rotations'], sym['translations'])]

        sites_0 = [[[c, c, c],
                    [c, c, c],
                    [c, c, c]]]
        sg_0 = SitesGrid(sites_0)
        cstru01 = CStru(m, sg_0)

        gen_01 = sogen.gen_nodup_cstru(m_tri, c, (1,3,3), t, 2)
        nodup_01 = [stru for stru in gen_01]
        self.assertEqual(len(nodup_01), 2)

        gen_02 = sogen.gen_nodup_cstru(m_tri, c, (1,3,3), t, 3)
        nodup_02 = [stru for stru in gen_02]
        self.assertEqual(len(nodup_02), 4)  

        gen_03 = sogen.gen_nodup_cstru(m_tri, c, (1,5,5), t, 2)
        nodup_03 = [stru for stru in gen_03]
        self.assertEqual(len(nodup_03), 4)  

    def test_is_speckle_disjunct(self):
        g = GhostSpecie()
        b = Specie('B')
        m = [[0, 0, 20],
             [1, 0, 0],
             [0.5, 0.8660254, 0]]
        # ele_sea = SitesGrid.sea(4, 4, 1, b)
        # cell_mother_stru = CStru(m, ele_sea).get_cell()
        # sym = get_symmetry(cell_mother_stru, symprec=1e-3)
        # ops = [(r, t) for r, t in zip(sym['rotations'], sym['translations'])]

        sites_0 = [[[g, g, b, b],
                    [b, b, b, b],
                    [b, b, b, b],
                    [b, b, b, b]]]
        sg_0 = SitesGrid(sites_0)
        cstru00 = CStru(m, sg_0)

        self.assertFalse(sogen.is_speckle_disjunct(cstru00, g))

        sites_1 = [[[g, b, b, g],
                    [b, b, b, b],
                    [b, b, b, b],
                    [b, b, b, b]]]
        sg_1 = SitesGrid(sites_1)
        cstru01 = CStru(m, sg_1)

        self.assertFalse(sogen.is_speckle_disjunct(cstru01, g))


        sites_2 = [[[g, b, b, b],
                    [b, g, b, b],
                    [b, b, b, b],
                    [b, b, b, b]]]
        sg_2 = SitesGrid(sites_2)
        cstru02 = CStru(m, sg_2)

        self.assertTrue(sogen.is_speckle_disjunct(cstru02, g))


if __name__ == "__main__":
    import nose2
    nose2.main()