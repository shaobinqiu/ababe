# coding: utf-8
# Distributed under the terms of the MIT License.

import numpy as np
# import collections

from ababe.stru.element import Specie, GhostSpecie

class Site(object):

    def __init__(self, atom=GhostSpecie(), value=None):
        if isinstance(atom, Specie):
            self._atom = atom
        elif atom == "G":
            self._atom = GhostSpecie()
        else: 
            self._atom = Specie(atom)

        self._value = value

    @property
    def value(self):
        """
        parameter for RL
        """
        return self._value

    @value.setter
    def value(self, v):
        self._value = v

    @property
    def atom(self):
        return self._atom

    @atom.setter
    def atom(self, sp):
        if isinstance(sp, Specie):
            self._atom = sp
        elif sp == "G":
            self._atom = GhostSpecie()
        else: 
            self._atom = Specie(sp)

    def copy(self):
        s = Site(self.atom, self.value)
        return s



class Grid(object):
    """
    Grid object. Used for constructed grids where to put the atoms on. 
    Like a chess board. 
    """

    def __init__(self, matrix, size=(2,2,2)):
        m = np.array(matrix, dtype=np.float64).reshape((3,3))
        lengths = np.sqrt(np.sum(m ** 2, axis=1))
        angles = np.zeros(3)
        for i in range(3):
            j = (i+1) % 3
            k = (i+2) % 3
            # angles[i] = abs_cap(dot(m[j], m[k]) / (lengths[j] * lengths[k]))

        self.length = size[0]
        self.width = size[1]
        self.height = size[2]
        self.sites = [[[Site() for _ in range(self.length)] 
                                        for _ in range(self.width)]
                                            for _ in range(self.height)]

    def dot():
        pass

    def get_site(self, position):
        (x,y) = position
        return self.sites[x][y]

    def get_shape(self):
        pass


