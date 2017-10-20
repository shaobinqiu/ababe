# coding: utf-8
# Distributed under the terms of the MIT License.
from .model import AppModel
from ababe.stru.scaffold import ModifiedCell
from ababe.stru.clarifier import VerboseAtomRemoveClarifier
from ababe.stru.element import Specie
from ababe.io.io import GeneralIO

import os
import numpy as np

class App(AppModel):

    def __init__(self, infile, processname, cenele, radius, ele, refined):
        gcell = GeneralIO.from_file(infile)
        self.mcell = ModifiedCell.from_gcell(gcell)

        self.pname = processname

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

        out = GeneralIO(gcell)
        ofname = "{:}_ACLR.vasp".format(self.pname.split('.')[0])

        print("PROCESSING: {:}".format(self.pname))
        out.write_file(ofname)
