# encoding: utf-8
# Distributed under the terms of the MIT License.

import nose
from nose.tools import *

import numpy as np
from spglib import get_symmetry
import ababe.utils.sogen as sogen
from ababe.stru.element import GhostSpecie, Specie
from ababe.stru.scaffold import SitesGrid, CStru
from ababe.stru.scaffold2d import SitesGrid2d, CStru2d

class testAlgorithomSog2d:

    # def setUp(self):
    #     pos_01 = 

    def test_get_id_seq2d(self):
        pass

    def test_update_isoset2d(self):
        pass

    def test_gen_nodup_cstru2d(self):
        pass

class testAlgorithomSog:

    # def setUp(self):
    #     pos_01 = 

    def test_get_id_seq(self):
        pos_0 = np.array([[ 0.        ,  0.        ,  0.        ],
                           [ 0.        ,  0.        ,  0.33333333],
                           [ 0.        ,  0.        ,  0.66666667],
                           [ 0.        ,  0.5       ,  0.        ],
                           [ 0.        ,  0.5       ,  0.33333333],
                           [ 0.        ,  0.5       ,  0.66666667]])

        pos_01 = np.array([[ 0.        ,  0.        ,  0.        ],
                           [ 0.        ,  0.        ,  0.66666667],
                           [ 0.        ,  0.        ,  0.33333333],
                           [ 0.        ,  0.5       ,  0.        ],
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
        eq_(len(s), 1)
        eq_(sogen._get_id_seq(pos_1, arr_num_00), a_id)

        eq_(a_id_01, a_id)
        eq_(a_id_02, a_id)


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

        sites_0 = [[[c, c],
                    [c, c]],

                   [[c, c],
                    [t, c]]]
        sg_0 = SitesGrid(sites_0)
        cstru01 = CStru(m, sg_0)

        isoset_init = set()
        isoset_init_copy = isoset_init.copy()
        isoset_a01 = sogen._update_isoset(isoset_init, cstru01, ops)
        assert_not_equal(isoset_a01, isoset_init_copy)
        ok_(isinstance(isoset_a01, set))

        isoset_a01_copy = isoset_a01.copy()
        isoset_a02 = sogen._update_isoset(isoset_a01, cstru01, ops)
        eq_(isoset_a02, isoset_a01_copy)
        ok_(len(isoset_a01) < len(ops))

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
        eq_(len(nodup_01), 1)

        # gen_02 = sogen.gen_nodup_cstru(m, c, (1,2,8), t, 4)
        # nodup_02 = [stru for stru in gen_02]
        # eq_(len(nodup_02), 51)

    def test_is_speckle_disjunct(self):
        g = GhostSpecie()
        b = Specie('B')
        m = [[1, 0, 0],
             [0.5, 0.866, 0],
             [0, 0, 20]]
        ele_sea = SitesGrid.sea(4, 4, 1, b)
        # cell_mother_stru = CStru(m, ele_sea).get_cell()
        # sym = get_symmetry(cell_mother_stru, symprec=1e-3)
        # ops = [(r, t) for r, t in zip(sym['rotations'], sym['translations'])]

        sites_0 = [[[g, g, b, b],
                    [b, b, b, b],
                    [b, b, b, b],
                    [b, b, b, b]]]
        sg_0 = SitesGrid(sites_0)
        cstru00 = CStru(m, sg_0)

        eq_(sogen.is_speckle_disjunct(cstru00, g), False)

        sites_1 = [[[g, b, b, g],
                    [b, b, b, b],
                    [b, b, b, b],
                    [b, b, b, b]]]
        sg_1 = SitesGrid(sites_1)
        cstru01 = CStru(m, sg_1)

        eq_(sogen.is_speckle_disjunct(cstru01, g), False)


        sites_2 = [[[g, b, b, b],
                    [b, b, b, b],
                    [b, g, b, b],
                    [b, b, b, b]]]
        sg_2 = SitesGrid(sites_2)
        cstru02 = CStru(m, sg_2)

        eq_(sogen.is_speckle_disjunct(cstru02, g), True)

if __name__ == "__main__":
    nose.main()