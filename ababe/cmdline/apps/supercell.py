# coding: utf-8
# Distributed under the terms of the MIT License.
from .model import AppModel
from ababe.stru.scaffold import GeneralCell
from ababe.stru.io import YamlOutput, VaspPOSCAR
import numpy as np

class App(AppModel):

    def __init__(self, settings, scale_matrix, zoom, outmode):
        """
        Now the input only support yaml config file.
        """
        lattice = np.array(settings['lattice'])
        positions = np.array(settings['positions'])
        numbers = np.array(settings['numbers'])
        self.cell = GeneralCell(lattice, positions, numbers)
        self.scale_matrix = np.array(scale_matrix)
        self.zoom = zoom
        self.outmode = outmode

    def run(self):
        #print('supercell running')
        # print(self.setting)
        sc = self.cell.supercell(self.scale_matrix)
        if self.outmode == 'yaml':
            beprint = YamlOutput(sc.spg_cell, self.zoom)
            print(beprint)
        elif self.outmode == 'vasp':
            beprint = VaspPOSCAR(sc.spg_cell, self.zoom)
            print(beprint)
