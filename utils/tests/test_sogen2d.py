# encoding: utf-8
# Distributed under the terms of the MIT License.

import nose
from nose.tools import *

import numpy as np
from spglib import get_symmetry
import ababe.utils.sogen2d as sogen2d
from ababe.stru.element import GhostSpecie, Specie
from ababe.stru.scaffold2d import SitesGrid2d, CStru2d

class testAlgorithomSog2d:

    # def setUp(self):
    #     pos_01 = 

    def test_get_id_seq2d(self):
        pos_0 = np.array([[0.   , 0.],
                            [0. , 0.333333 ],
                            [0. , 0.666667 ],
                            [0.333333, 0. ],
                            [0.333333, 0.333333 ],
                            [0.333333, 0.666667],
                            [0.666666, 0. ],
                            [0.666666, 0.333333 ],
                            [0.666666, 0.666666 ]])
        arr_num_00 = np.array([n for n in np.array([[22, 22, 22],
                                                    [22, 22, 22],
                                                    [22, 22, 22]]).flat])

        a_id = sogen._get_id_seq(pos_0, arr_num_00)

        pos_01 = np.array([[0.   , 0.],
                            [0. , 0.333333 ],
                            [0. , 0.666667 ],
                            [0.333333, 0. ],
                            [0.333333, 0.333333 ],
                            [0.333333, 0.666667],
                            [0.666666, 0. ],
                            [0.666666, 0.333333 ],
                            [0.666666, 0.666666 ]])


    def test_update_isoset2d(self):
        pass

    def test_gen_nodup_cstru2d(self):
        c = Specie("Cu")
        t = Specie("Ti")
        m = [[1.0, 0.0],
             [0.5, 0.866]]
