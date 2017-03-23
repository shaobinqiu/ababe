# coding: utf-8
# Distributed under the terms of the MIT License.

from ababe.stru.scaffold2d import SitesGrid2d, CStru2d
from ababe.stru.element import GhostSpecie, Specie
import numpy as np

import unittest, nose
from nose.tools import *

class TestSitesGrid2d:

    def setUp(self):
        g = GhostSpecie()
        b = Specie("B")
        self.sites = [  [g,g,g,b,g],
                        [g,g,b,b,g],
                        [b,b,b,g,b],
                        [g,g,b,b,g]]

        self.sg = SitesGrid2d(self.sites)
        self.allg = SitesGrid2d.sea(4, 5, GhostSpecie())

    def test_equal(self):
        other_eq = SitesGrid2d(self.sites)
        eq_(other_eq, self.sg)
        assert_not_equal(None, self.sg)
        assert_not_equal(self.allg, self.sg)

    def test_get_array(self):
        a = np.array([0]*20).reshape((4,5))
        ok_(np.allclose(self.allg.get_array(), a))
        b = np.array([0,0,0,5,0,0,0,5,5,0,5,5,5,0,5,0,0,5,5,0]).reshape((4,5))
        ok_(np.allclose(self.sg.get_array(), b))

    def test_from_array(self):
        arr = np.array([0,0,0,5,0,0,0,5,5,0,5,5,5,0,5,0,0,5,5,0]).reshape((4,5))
        ss = SitesGrid2d.from_array(arr)
        eq_(ss, self.sg)

class TestCStru2d:

    def setUp(self):
        g = GhostSpecie()
        b = Specie("B")
        self.m = [[2, 0], [1, 1.732058]]
        sites = [   [g,g,g,b,g],
                    [g,g,b,b,g],
                    [b,b,b,g,b],
                    [g,g,b,b,g] ]
        self.sg = SitesGrid2d(sites)
        self.s = CStru2d(self.m, self.sg)

    def test_get_midpoint(self):
        eq_(self.s.get_midpoint(), (2, 2))

    def test_get_neighbors(self):
        eq_(self.s.get_neighbors((1,2), 2.1), 
                    set([(0,2), (2,2), (1,1), (1,3), (0,3), (2,1)]))
        eq_(len(self.s.get_neighbors((0,4), 2.1)), 3)
        eq_(len(self.s.get_neighbors((3,4), 2.1)), 2)
        eq_(len(self.s.get_neighbors((1,0), 20)), 19)


        