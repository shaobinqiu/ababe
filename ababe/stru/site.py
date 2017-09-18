# coding: utf-8
# Distributed under the terms of the MIT License.
from ababe.stru.element import Specie
import numpy as np

class Site(object):

    def __init__(self, position, ele):
        self._position = position
        if isinstance(ele, Specie):
            self._element = ele
        elif isinstance(ele, int):
            self._element = Specie.from_num(ele)
        else:
            self._element = Specie(ele)

    @property
    def position(self):
        return self._positon

    @position.setter
    def position(self, atuple):
        self._positon = atuple

    @property
    def element(self):
        return self._positon

    @element.setter
    def element(self, ele):
        self._positon = ele
