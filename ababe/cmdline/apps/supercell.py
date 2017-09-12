# coding: utf-8
# Distributed under the terms of the MIT License.
from .model import Appmodel
from ababe.stru.scaffold import GeneralCell
from ababe.stru.io import YamlOutput, VaspPOSCAR
import numpy as np

class App(Appmodel):

    def __init__(self, settings, scale_matrix, zoom):
        """
        Now the afile only support yaml config file.
        """
        lattice = np.array(settings['lattice'])
        positions = np.array(settings['positions'])
        numbers = np.array(settings['numbers'])
        self.cell = GeneralCell(lattice, positions, numbers)
        self.scale_matrix = np.array(scale_matrix)
        self.zoom = zoom

    def run(self, outmode):
        #print('supercell running')
        # print(self.setting)
        sc = self.cell.supercell(self.scale_matrix)
        if outmode == 'yaml':
            beprint = YamlOutput(sc.spg_cell, self.zoom)
            print(beprint)
        elif outmode == 'vasp':
            beprint = VaspPOSCAR(sc.spg_cell, self.zoom)
            print(beprint)
