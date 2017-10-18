# coding: utf-8
# Distributed under the terms of the MIT License.
from .model import AppModel
from ababe.stru.scaffold import ModifiedCell
from ababe.stru.element import Specie
from ababe.stru.io import VaspPOSCAR

import os
import numpy as np

class App(AppModel):

    def __init__(self, settings, fname, radius):
        try:
            zoom = settings['zoom']
        except:
            zoom = 1
        latt = np.array(settings['lattice'])*zoom
        pos = np.array(settings['positions'])
        numbers = np.array(settings['numbers'])
        self.mcell = ModifiedCell(latt, pos, numbers)

        self.radius = radius
        self.fname = fname

    def run(self):
        import tempfile
        working_path = os.getcwd()

        self.mcell.perturb(self.radius)
        gcell = self.mcell.to_gcell()

        out = VaspPOSCAR(gcell, 1)
        tf = tempfile.NamedTemporaryFile(mode='w+b', dir=working_path, prefix='POSCAR_',
                                         suffix='.MOD.vasp', delete=False)
        print("PROCESSING: {:}".format(self.fname))
        out.write(tf.name)
