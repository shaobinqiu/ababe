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

    def __init__(self, settings, filename, cenele, radius, ele, refined):
        try:
            zoom = settings['zoom']
        except:
            zoom = 1
        latt = np.array(settings['lattice'])*zoom
        pos = np.array(settings['positions'])
        numbers = np.array(settings['numbers'])
        self.mcell = ModifiedCell(latt, pos, numbers)

        self.fname = filename

        self.clarifier = VerboseAtomRemoveClarifier(Specie(cenele), radius, Specie(ele))
        self.refined = refined

    def run(self):
        import tempfile
        working_path = os.getcwd()

        new_mcell = self.clarifier.clarify(self.mcell)
        gcell = new_mcell.to_gcell()
        # todo: add feature- to convcell.
        if self.refined:
            gcell = gcell.get_refined_pcell()

        out = VaspPOSCAR(gcell, 1)
        tf = tempfile.NamedTemporaryFile(mode='w+b', dir=working_path, prefix='POSCAR_',
                                         suffix='.MOD.vasp', delete=False)
        print("PROCESSING: {:}".format(self.fname))
        out.write(tf.name)
