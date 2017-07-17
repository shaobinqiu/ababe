# coding: utf-8
# Distributed under the terms of the MIT License.

from ababe.stru.scaffold import SitesGrid, CStru, GeneralCell
from ababe.stru.element import GhostSpecie, Specie
import numpy as np

import unittest

class testSitesGrid(unittest.TestCase):

    def setUp(self):
        g = GhostSpecie()
        b = Specie("B")
        self.sites   = [[[b, b],
                    [g, g]],

                   [[b, g],
                    [g, b]]]
        self.sg = SitesGrid(self.sites)
        self.allg0 = SitesGrid.sea(2, 2, 2, GhostSpecie())
        self.allg = SitesGrid.sea(4, 2, 2, GhostSpecie())

    def test_properties(self):
        # ok_(np.allclose(self.g.base_vector, 
                        # np.array(m, dtype=np.float64).reshape((3,3))))
        self.assertEqual(self.allg.depth, 4)
        self.assertEqual(self.allg.length, 2)
        self.assertEqual(self.allg.width, 2)
        self.assertEqual(self.sg.sites, self.sites)

    def test_get(self):
        self.assertEqual(self.sg[0, 1, 1], GhostSpecie())

        self.sg[0, 1, 1] = Specie("B")
        self.assertEqual(self.sg[0, 1, 1], Specie("B"))

    def test_equal(self):
        other = SitesGrid.sea(4, 2, 2, Specie("Ti"))
        self.assertNotEqual(other, self.allg)
        self.assertNotEqual(None, self.allg)

    def test_deepCopy(self):
        g_copy = self.allg.deepCopy()
        self.assertEqual(g_copy, self.allg)
        self.assertNotEqual(id(g_copy), id(self.allg))
        # assert_not_equal(id(g_copy[0, 0, 0]), id(g_copy[0, 0, 0]))

    def test_hash(self):
        pass

    def test_to_array(self):
        a = np.array([0]*8).reshape((2,2,2))
        self.assertTrue(np.allclose(self.allg0.to_array(), a))
        b = np.array([5,5,0,0,5,0,0,5]).reshape((2,2,2))
        self.assertTrue(np.allclose(self.sg.to_array(), b))

    def test_from_array(self):
        arr = np.array([5,5,0,0,5,0,0,5]).reshape([2,2,2])
        ss = SitesGrid.from_array(arr)
        self.assertEqual(ss, self.sg)

    def test_random_fill(self):
        r = SitesGrid.random_fill(GhostSpecie(), (2,2,2), Specie("B"))
        self.assertIn(r.to_array().sum(), [5*x for x in range(9)])

    def test_gen_speckle(self):
        c = Specie("Cu")
        t = Specie("Ti")
        sites   = [[[c, c],
                    [t, t]],

                   [[c, t],
                    [t, c]]]
        self.sg = SitesGrid(sites)
        gen = SitesGrid.gen_speckle(Specie("Cu"), (2,2,2), Specie("Ti"), 4)
        from collections import Iterator
        self.assertIsInstance(gen, Iterator)
        self.assertIn(self.sg, gen)
        self.assertEqual(next(gen).to_array().sum(), 204)
        self.assertEqual(next(gen).to_array().sum(), 204)

class testCStru(unittest.TestCase):

    def setUp(self):
        self.m = [[1,0,0],[0,1,0],[0,0,1]]
        g = GhostSpecie()
        b = Specie("B")
        self.sites = [[[g, b], 
                  [g, g]],

                 [[b, b],
                  [b, g]]]

        self.arr = np.array([0,5,0,0,5,5,5,0]).reshape([2,2,2])
        self.sg = SitesGrid(self.sites)
        self.s = CStru(self.m, self.sg)

    def test_get_property(self):
        self.assertEqual(self.s.m, self.m)
        # eq_(self.s.depth, 2)
        # eq_(self.s.width, 2)
        # eq_(self.s.length, 2)

        # eq_(self.s.get_grid, self.sites)
        # arr = [[[0, 5],
        #         [0, 0]],

        #        [[5, 5],
        #         [5, 0]]]
        # eq_(self.s.get_array(), arr)

    def test_equal(self):
        m_0 = [[1,1,1], [0,0,1], [1,0,0]]
        g = GhostSpecie()
        b = Specie("B")
        sites_0 = [[[b, b],
                    [g, g]],

                   [[b, g],
                    [g, b]]]
        sg_0 = SitesGrid(sites_0)

        diff_m = CStru(m_0, self.sg)
        diff_s = CStru(self.m, sg_0)
        self.assertEqual(self.s, self.s)
        self.assertNotEqual(diff_m, self.s)
        self.assertNotEqual(diff_s, self.s)

    def test_from_array(self):
        ss = CStru.from_array(self.m, self.arr)
        self.assertEqual(ss, self.s)

    def test_get_array(self):
        self.assertTrue(np.allclose(self.s.get_array(), self.arr))

    def test_gen_speckle(self):
        c = Specie("Cu")
        t = Specie("Ti")
        sites   = [[[c, c],
                    [t, t]],

                   [[c, t],
                    [t, c]]]
        sg = SitesGrid(sites)
        gen = CStru.gen_speckle(self.m, Specie("Cu"), (2,2,2), Specie("Ti"), 4)
        from collections import Iterator
        self.assertIsInstance(gen, Iterator)
        self.assertIn(CStru(self.m, sg), gen)
        self.assertEqual(next(gen).get_array().sum(), 204)
        self.assertEqual(next(gen).get_array().sum(), 204)

    def test_get_cell(self):
        c = Specie("Cu")
        t = Specie("Ti")
        m = [[-0.5, -0.5, -0.5],
             [-0.5,  0.5,  0.5],
             [ 0.5, -0.5,  0.5]]

        sites01 = [[[c]]]
        sites02 = [[[t, c, t],
                    [t, t, c]]]
        sg01 = SitesGrid(sites01)
        sg02 = SitesGrid(sites02)
        cstru01 = CStru(m, sg01)
        cstru02 = CStru(m, sg02)
        lat01, pos01, num01 = cstru01.get_cell()
        lat02, pos02, num02 = cstru02.get_cell()
        self.assertTrue(np.allclose(lat01, np.array([[-0.5, -0.5, -0.5],
                                                    [-0.5,  0.5,  0.5],
                                                    [ 0.5, -0.5,  0.5]])))
        self.assertTrue(np.allclose(pos01, np.array([[0, 0, 0]])))
        self.assertTrue(np.allclose(num01, np.array([29])))

        self.assertTrue(np.allclose(lat02, np.array([[-0.5, -0.5, -0.5],
                                          [-1,  1,  1],
                                         [ 1.5, -1.5,  1.5]])))
        self.assertTrue(np.allclose(pos02, np.array([[0, 0, 0],
                                         [0, 0, 1/3],
                                         [0, 0, 2/3],
                                         [0, 1/2, 0],
                                         [0, 1/2, 1/3],
                                         [0, 1/2, 2/3]])))
        self.assertTrue(np.allclose(num02, np.array([22, 29, 22, 22, 22, 29])))


class testGeneralCell(unittest.TestCase):

    def setUp(self):
        arr_lat = np.array([[3.0, 0, 0], [0, 2.0, 0.0], [0, 0, 1.0]])
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
        arr_positions = np.array(positions)
        arr_numbers = np.array([6]*12)
        self.cell = GeneralCell(arr_lat, arr_positions, arr_numbers)

    def test_property(self):
        np.testing.assert_equal(self.cell.numbers, np.array([6]*12))

    def test_get_symmetry(self):
        sym = self.cell.get_spacegroup()
        self.assertEqual(sym, 'Im-3m (229)')

    def test_get_symmetry_permutation(self):
        sym_num = len(self.cell.get_symmetry_permutation())
        self.assertEqual(sym_num, 96)


if __name__ == "__main__":
    import nose2
    nose2.main()