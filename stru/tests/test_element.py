# coding: utf-8
# Distributed under the terms of the MIT License.

import unittest
import nose
from nose.tools import *

from ababe.stru.element import Specie, GhostSpecie

class SpecieTestCase(unittest.TestCase):

    def setUp(self):
        self.b = Specie("B")

    def test_properties(self):
        eq_(self.b.symbol, "B")
        eq_(self.b.Z, 5)
        eq_(self.b.atom_mass, 10.811)
        eq_(self.b.atom_radius, 0.85)

class GhostSpecieTestCase:

    def setUp(self):
        self.g = GhostSpecie()

    def test_properties(self):
        ok_(isinstance(self.g, Specie))
        eq_(self.g.symbol, "G")
        eq_(self.g.Z, 0)
        eq_(self.g.atom_mass, 0)
        eq_(self.g.atom_radius, 0)

if __name__ == "__main__":
    nose.main()