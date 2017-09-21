# coding: utf-8
# Distributed under the terms of the MIT License.
from .model import AppModel
from ababe.stru.element import Specie
from ababe.stru.scaffold import GeneralCell
from ababe.stru.sogen import OccupyGenerator
from ababe.stru.io import VaspPOSCAR
from ababe.stru.restriction import MinDistanceRestriction

import numpy as np
import os

class App(AppModel):

    def __init__(self, settings, comment, element, speckle, nspeckle, zoom, trs):
        # read comment & zoom from setting file first
        # if not exist, read from cmd args, then default
        if zoom is None:
            try:
                zoom = settings['zoom']
            except:
                zoom = 1
        self.zoom = zoom

        if comment is None:
            try:
                comment = settings['comment']
            except:
                comment = 'default'
        self.comment = comment

        lat = np.array(settings['lattice'])
        pos = np.array(settings['positions'])
        num = np.array(settings['numbers'])
        self.cell = GeneralCell(lat*self.zoom, pos, num)

        self.element = element

        # Get number and index of target element
        if element is None:
            tgt_ele = int(num[1])
        else:
            tgt_ele = Specie(element).Z
        tgt_ele_index = np.where(num == tgt_ele)[0]

        if speckle is None:
            self.speckle = Specie('G')
        else:
            self.speckle = Specie(speckle)

        # self.ele for function all-speckle-gen-of-ele in run
        self.ele = Specie.from_num(tgt_ele)

        if nspeckle is None:
            # If not given speckle to number most - 1
            self.nmax = tgt_ele_index.size - 1
        else:
            self.nmax = nspeckle
        # if there no restriction given then no restriction
        if trs != ():
            self.tr = trs[0]
        else:
            self.tr = None

    def run(self):
        # Create directory contain POSCARs
        import random
        import string
        import tempfile

        rd_suffix = ''.join(random.choices(string.ascii_uppercase
                                           + string.digits, k=5))
        working_path = os.getcwd()
        poscars_dir = os.path.join(working_path,
                                   'POSCARs_{0:}_{1:}'.format(self.comment,
                                                              rd_suffix))
        if not os.path.exists(poscars_dir):
            os.makedirs(poscars_dir)
        else:
            shutil.rmtree(poscars_dir)
            os.makedirs(poscars_dir)

        ogg = OccupyGenerator(self.cell)
        gg = ogg.all_speckle_gen_of_ele(self.nmax, self.ele, self.speckle)

        if self.tr is not None:
            tr = (Specie(self.tr[0]), self.tr[1])
            applied_restriction = MinDistanceRestriction(tr)

        for i, outer_gen in enumerate(gg):
            # print("Processing: {0:3}s substitue {1:2d}...".format(speckle, i+1))
            for n_count, c in enumerate(outer_gen):
                if self.tr is not None:
                    condition = c.is_primitive() and applied_restriction.is_satisfied(c)
                else:
                    condition = c.is_primitive()

                if condition:
                    # c = c.get_refined_pcell()
                    poscar = VaspPOSCAR(c, 1)
                    tf = tempfile.NamedTemporaryFile(mode='w+b', dir=poscars_dir,
                                                     prefix='POSCAR_S{:}_'
                                                            .format(i+1),
                                                     suffix='.vasp', delete=False)
                    poscar.write(tf.name)
