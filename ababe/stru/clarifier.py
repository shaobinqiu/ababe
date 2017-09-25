# coding: utf-8
# Distributed under the terms of the MIT License.
import numpy as np

from ababe.stru.scaffold import ModifiedCell

class Clarifier(object):

    def __init__(self):
        pass

    def clarifier(self, modecell):
        pass

class AtomRemoveClarifier(Clarifier):

    def __init__(self, center, r, element=None):
        self.center = np.array(center)
        self.element = element
        self.r = r

    def clarify(self, modcell):
        if not isinstance(modcell, ModifiedCell):
            raise ValueError('Please input a ModifiedCell')

        dsites = modcell.get_points_incell_insphere(self.center, self.r, self.element)
        modcell.remove_sites(list(dsites.keys()))
        return modcell
