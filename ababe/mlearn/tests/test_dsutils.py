# coding: utf-8
# Distributed under the terms of the MIT License.

import random

from ababe.mlearn.dsutils import RandomPopSet
import nose

from nose.tools import *
# from unittest.mock import patch

# @patch('random.randint', return_value=3)
class test_random_pop_set:

    def setUp(self):
        self.rp = RandomPopSet()
        self.rp_nn = RandomPopSet([2,4,5,5,1])

    def test_add(self):
        rp = RandomPopSet()
        rp.add(5)
        rp.add(5)
        eq_(rp, RandomPopSet([5]))
        rp.add(34)
        eq_(rp, RandomPopSet([5, 34]))

    def test_len(self):
        eq_(len(self.rp_nn), 4)
        eq_(len(self.rp), 0)

    def test_discard(self):
        rp_nn = RandomPopSet([2,4,5,5,1])
        rp_nn.discard(2)
        eq_(rp_nn, RandomPopSet([5,5,5,1,4]))

    def test_random_pop(self):
        rp_nn = RandomPopSet([2,4,5,5,1])
        random.seed(0)
        eq_(rp_nn.random_pop(), 1)
        eq_(rp_nn, RandomPopSet([2,4,5]))

if __name__ == "__main__":
    nose.main()
