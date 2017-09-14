# coding: utf-8
# Distributed under the terms of the MIT License.
from .model import AppModel
from ababe.stru.scaffold import GeneralCell
from ababe.stru.io import YamlOutput, VaspPOSCAR
from ababe.stru.grid import SuperLatticeGenerator
import numpy as np
import os
import shutil

class App(AppModel):

    def __init__(self, settings, comment, volumn, zoom, outmode):
        ulat = np.array(settings['lattice'])
        upos = np.array(settings['positions'])
        unum = np.array(settings['numbers'])
        self.ucell = (ulat, upos, unum)
        self.v = volumn

        if comment is None:
            try:
                comment = settings['comment']
            except:
                comment = 'default'
        self.comment = comment

        if zoom is None:
            try:
                zoom = settings['zoom']
            except:
                zoom = 1
        self.zoom = zoom

        self.outmode = outmode

    def run(self):
        import tempfile

        hnfs = SuperLatticeGenerator.hnfs_from_n(self.ucell, self.v)
        # Create a dir contains suplat files
        working_path = os.getcwd()
        suplat_dir = os.path.join(working_path,
                                        'SUPLAT_{:}'.format(self.comment))
        if not os.path.exists(suplat_dir):
            os.makedirs(suplat_dir)
        else:
            shutil.rmtree(suplat_dir)
            os.makedirs(suplat_dir)

        # For diff outmode
        if self.outmode == 'vasp':
            Output = VaspPOSCAR
            suffix = '.vasp'
        else:
            Output = YamlOutput
            suffix = '.yaml'

        for hnf in hnfs:
            sl = hnf.to_general_cell()
            out = Output(sl, self.zoom)
            tf = tempfile.NamedTemporaryFile(mode='w+b', dir=suplat_dir,
                                             prefix='SUPLAT_{:}_'.
                                             format(self.v),
                                             suffix=suffix, delete=False)
            out.write(tf.name)
