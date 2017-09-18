# coding: utf-8
# Distributed under the terms of the MIT License.
from ababe.stru.site import Site
from ababe.stru.element import Specie
import unittest

class TestSite(unittest.TestCase):

    def test_init(self):
        s = Site((1,2,0), 'S')
        s = Site((1,2,0), Specie('S'))
        s = Site((1,2,0), 16)

    def test_error_init(self):
        pass
