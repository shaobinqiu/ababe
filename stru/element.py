# coding: utf-8
# Distributed under the terms of the MIT License.
import os
import json

from enum import Enum

# Loads periodic_table database from json file pt.json
with open(os.path.join(os.path.dirname(__file__),
                            "pt.json"), "rt") as f:
    _pt_db = json.load(f)

class Specie(object):

    def __init__(self, symbol):
        self.symbol = "%s" % symbol
        d = _pt_db[symbol]

        self.Z = d["Atomic no"]
        self.atom_mass = d["Atomic mass"]
        self.atom_radius = d["Atomic radius"]

class GhostSpecie(Specie):
    """
    A special species for representing vacancies
    """

    def __init__(self):
        self.symbol = "G"
        self.Z = 0
        self.atom_mass = 0
        self.atom_radius = 0