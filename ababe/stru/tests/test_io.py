# encoding: utf-8
# Distributed under the terms of the MIT License.

import nose
from nose.tools import *
import os
import unittest

import numpy as np
from math import sqrt
from ababe.stru.scaffold import CStru
from ababe.stru.io import VaspPOSCAR

# test_dir = os.path.join(os.path.dirname(__file__), 'test_files')

class testVaspPOSCAR(object):

    def test_get_string(self):
        boron_arr = np.array([[[5,0,5,5,5,5],
                               [5,5,5,5,5,5],
                               [5,5,0,5,5,5]]])
        latt = [[0, 0, 20],
                [1, 0, 0],
                [0.5, sqrt(3)/2, 0]]
        boron_stru = CStru.from_array(latt, boron_arr)
        poscar = VaspPOSCAR(boron_stru)

        expected_str = '''B16
1.0
  0.000000   0.000000  20.000000
  3.000000   0.000000   0.000000
  3.000000   5.196152   0.000000
B
16
direct
  0.000000   0.000000   0.000000 B
  0.000000   0.000000   0.333333 B
  0.000000   0.000000   0.500000 B
  0.000000   0.000000   0.666667 B
  0.000000   0.000000   0.833333 B
  0.000000   0.333333   0.000000 B
  0.000000   0.333333   0.166667 B
  0.000000   0.333333   0.333333 B
  0.000000   0.333333   0.500000 B
  0.000000   0.333333   0.666667 B
  0.000000   0.333333   0.833333 B
  0.000000   0.666667   0.000000 B
  0.000000   0.666667   0.166667 B
  0.000000   0.666667   0.500000 B
  0.000000   0.666667   0.666667 B
  0.000000   0.666667   0.833333 B
'''
        eq_(str(poscar), expected_str)

        bcu_arr = np.array([[[5,29,5,5,5,5],
                               [5,5,5,5,5,5],
                               [5,5,29,5,5,5]]])
        latt = [[0, 0, 20],
                [1, 0, 0],
                [0.5, sqrt(3)/2, 0]]
        bcu_stru = CStru.from_array(latt, bcu_arr)
        poscar_bcu = VaspPOSCAR(bcu_stru)

        expected_str_bcu = '''B16Cu2
1.0
  0.000000   0.000000  20.000000
  3.000000   0.000000   0.000000
  3.000000   5.196152   0.000000
B Cu
16 2
direct
  0.000000   0.000000   0.000000 B
  0.000000   0.000000   0.333333 B
  0.000000   0.000000   0.500000 B
  0.000000   0.000000   0.666667 B
  0.000000   0.000000   0.833333 B
  0.000000   0.333333   0.000000 B
  0.000000   0.333333   0.166667 B
  0.000000   0.333333   0.333333 B
  0.000000   0.333333   0.500000 B
  0.000000   0.333333   0.666667 B
  0.000000   0.333333   0.833333 B
  0.000000   0.666667   0.000000 B
  0.000000   0.666667   0.166667 B
  0.000000   0.666667   0.500000 B
  0.000000   0.666667   0.666667 B
  0.000000   0.666667   0.833333 B
  0.000000   0.000000   0.166667 Cu
  0.000000   0.666667   0.333333 Cu
'''
        eq_(str(poscar_bcu), expected_str_bcu)

    def test_write_file(self):
        """.
        The function is tested by save structure
        to a POSCAR file, and then read from it.
        Compare the parameters read from to the 
        origin input parameter. Using almostEqual
        """
        bcu_arr = np.array([[[5,29,5,5,5,5],
                               [5,5,5,5,5,5],
                               [5,5,29,5,5,5]]])
        latt = [[0, 0, 20],
                [1, 0, 0],
                [0.5, sqrt(3)/2, 0]]
        bcu_stru = CStru.from_array(latt, bcu_arr)
        poscar_bcu = VaspPOSCAR(bcu_stru)

        tmp_file = "POSCAR.testing"
        poscar_bcu.write_POSCAR(tmp_file)

        with open(tmp_file, 'r') as testing_file:
            data = testing_file.read()

        eq_(data, str(poscar_bcu))
        os.remove(tmp_file)

if __name__ == "__main__":
    nose.main()