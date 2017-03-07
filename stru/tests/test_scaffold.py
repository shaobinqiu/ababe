# coding: utf-8
# Distributed under the terms of the MIT License.

from ababe.stru.scaffold import Grid, Site, StruState
from ababe.stru.element import GhostSpecie, Specie
import numpy as np

import unittest, nose
from nose.tools import *

class SiteTestCase(unittest.TestCase):

    def setUp(self):
        self.s1 = Site("Cu", value=1)
        self.s2 = Site("Ti", value=None)
        self.s3 = Site("B")
        self.sg = Site("G")

    def test_init(self):
        eq_(Site(), Site("G"))

    def test_properties(self):
        ok_(isinstance(self.sg, Site))
        ok_(isinstance(self.s1, Site))


    def test_value(self):
        eq_(self.s1.value, 1)
        ok_(self.s2.value is None)
        ok_(self.s3.value is None)

        new_s1 = self.s1.copy()
        eq_(new_s1.value, 1)
        new_s1.value = 20
        eq_(new_s1.value, 20)
        eq_(self.s1.value, 1)

    def test_atom(self):
        s = self.s2
        eq_(s.atom.symbol, "Ti")
        eq_(s.atom.Z, 22)
        g = self.sg
        eq_(g.atom.Z, 0)
        
        # atom on site can be reset
        g.atom = "Ti"
        eq_(g.atom.Z, s.atom.Z)

class GridTestCase(unittest.TestCase):

    def setUp(self):
        m = [[1,0,0],[0,1,0],[0,0,1]]
        size = (1,2,4)
        self.g = Grid(m, size)

    def test_properties(self):
        ok_(np.allclose(self.g.base_vector, 
                        np.array(m, dtype=np.float64).reshape((3,3))))
        eq_(self.g.length, 1)
        eq_(self.g.width, 2)
        eq_(self.g.height, 4)

class StruStateTestCase(unittest.TestCase):

    def setUp(self):
        self.m = [[1,0,0],[0,1,0],[0,0,1]]
        vac = Site()
        b = Site(Specie("B"))
        s_mat = StruState.create_sea(GhostSpecie(), size=(2,2,3))
        self.s_ifm =   [[[vac,vac], [vac,vac]], 
                            [[b,b], [b,b]],
                            [[b,vac], [bac,b]]] # 2x2x3 sites_information
        self.init_stru = StruState(basis = self.grid_basis, size = (2,2,3), sites_mat = s_mat)

    def test_init_from_grid():
        constru_grid = Grid(self.m, size = (2,2,3))
        s_from_grid = StruState.from_grid(constructed, sites_mat = s_mat)        
        eq_(s_from_grid, self.init_stru)

    def test_arrange_sites(self):
        self.new_stru = self.init_stru.arrange_sites(self.s_ifm)

        # to constructed new stru, should be deepCopy???
        assert_not_equal(id(self.new_stru), id(self.init_stru))
        assert_not_equal(id(self.new_stru[0][0][0]), id(self.init_stru[0][0][0]))

    def test_get_site(self):
        positon = (1,0,2)
        eq_(self.new_stru.get_site(position).atom, GhostSpecie())
        eq_(self.new_stru.get_site(position).value, 0)

    def test_mat2sites(self):
        pass

    def test_sites2mat(self):
        pass

    def test_random_fill(self):
        pass
        
if __name__ == "__main__":
    nose.main()