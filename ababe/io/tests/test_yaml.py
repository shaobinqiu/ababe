# coding: utf-8
# Distributed under the terms of the MIT License.
import unittest
import os
import numpy as np

from ababe.io.yaml import YamlInput, YamlOutput
from ababe.stru.scaffold import GeneralCell

testdata_dir = os.path.join(os.path.dirname(__file__), "test_files")

class TestYamlInput(unittest.TestCase):

    def setUp(self):
        self.filename = os.path.join(testdata_dir, "zns.yaml")

    def test_init(self):
        yaml_in = YamlInput(self.filename)

    def test_get_gcell(self):
        yaml_in = YamlInput(self.filename)
        gcell = yaml_in.get_cell()

        expect_latt = np.array([[0., 0.5, 0.5],
                                [0.5, 0., 0.5],
                                [0.5, 0.5, 0.]])
        expect_positions = np.array([[0., 0., 0.],
                                     [0.25, 0.25, 0.25])
        expect_numbers = np.array([30, 16])
        self.assertTrue(np.allclose(gcell.lattice, expect_latt))
        self.assertTrue(np.allclose(gcell.positions, expect_positions))
        self.assertTrue(np.allclose(gcell.numbers, expect_numbers))


class TestYamlOutput(unittest.TestCase):

    def setUp(self):
        latt = np.array([[0., 0.5, 0.5],
                         [0.5, 0., 0.5],
                         [0.5, 0.5, 0.]])
        positions = np.array([[0., 0., 0.],
                              [0.25, 0.25, 0.25])
        numbers = np.array([30, 16])
        cell = GeneralCell(latt, positions, numbers)
        self.yaml_out = YamlOutput(cell, comment=None, zoom=3)

    def test_get_string(self):
        expected_str = '''comment: S6Zn2
lattice:
- [0.000000, 0.500000, 0.500000]
- [0.500000, 0.000000, 0.500000]
- [0.500000, 0.500000, 0.000000]
positions:
- [0.250000, 0.250000, 0.250000]
- [0.000000, 0.000000, 0.000000]
numbers: [16, 30]
zoom: 3
'''
        self.assertEqual(str(self.yaml_out), expected_str)

    def test_write_file(self):
        """.
        The function is tested by save structure
        to a POSCAR file, and then read from it.
        Compare the parameters read from to the
        origin input parameter. Using almostEqual
        """
        tmp_file = os.path.join(testdata_dir, "testing.yaml")
        self.yaml_out.write(tmp_file)

        with open(tmp_file, 'r') as testing_file:
            data = testing_file.read()

        self.assertEqual(data, str(self.yaml_out))
        os.remove(tmp_file)


if __name__ = "__main__":
    import nose2
    nose2.main()
