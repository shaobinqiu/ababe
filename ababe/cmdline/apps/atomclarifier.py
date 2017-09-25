# coding: utf-8
# Distributed under the terms of the MIT License.
from .model import AppModel
from ababe.stru.scaffold import ModifiedCell
from ababe.stru.clarifier import VerboseAtomRemoveClarifier
from ababe.stru.element import Specie
from ababe.stru.io import VaspPOSCAR

import os
import numpy as np

class App(AppModel):

    def __init__(self, settings, filename, cenele, radius, ele):
        zoom = settings['zoom']
        latt = np.array(settings['lattice'])*zoom
        pos = np.array(settings['positions'])
        numbers = np.array(settings['numbers'])
        self.mcell = ModifiedCell(latt, pos, numbers)

        self.fname = filename

        self.clarifier = VerboseAtomRemoveClarifier(Specie(cenele), radius, Specie(ele))

    def run(self):
        import tempfile
        working_path = os.getcwd()

        new_mcell = self.clarifier.clarify(self.mcell)
        gcell = new_mcell.to_gcell()

        out = VaspPOSCAR(gcell, 1)
        tf = tempfile.NamedTemporaryFile(mode='w+b', dir=working_path,
                                         suffix='.MOD.vasp', delete=False)
        out.write(tf.name)
