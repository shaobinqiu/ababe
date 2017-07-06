# coding: utf-8
# Distributed under the terms of the MIT license.
import os
import json

import numpy as np
import spglib

from ababe.stru.element import Specie

# Loads bucky-ball structure data from json file
with open(os.path.join(os.path.dirname(__file__),
                            "buckyball.json"), "rt") as f:
    _buckyball = json.load(f)

class Structure(object):
    """
    Class to generate bucky-ball related structure parameters.
    """

    def __init__(self, numbers):
        self._lattice = np.array(_buckyball["lattice"])

        # Sorting positions (x,y,z)
        init_positions = np.array(_buckyball["positions"])
        init_index = self._get_new_id_seq(init_positions, numbers)
        self._positions = init_positions[init_index]

        self._atom_numbers = numbers
        self._spg_cell = (self._lattice, self._positions, self._atom_numbers)
        self._carbon = Specie("C")

    @property
    def spg_cell(self):
        return self._spg_cell

    def get_spacegroup(self):
        return spglib.get_spacegroup(self._spg_cell, symprec=1e-4)

    def get_speckle_num(self, sp):
        atom = sp.Z
        num = self._atom_numbers.count(atom)
        return num

    def get_symmetry(self):
        """
        Symmetry operations are obtained as a dictionary. 
        The key rotation contains a numpy array of integer, 
        which is “number of symmetry operations” x “3x3 matrices”. 
        The key translation contains a numpy array of float, 
        which is “number of symmetry operations” x “vectors”. 
        """
        symmetry = spglib.get_symmetry(self._spg_cell, symprec=1e-4)
        return symmetry

    def get_symmetry_permutation(self):
        """
        This a object function to get the permutation group operators.
        Represented as a table.
        """
        sym_perm = []
        numbers = [i for i in range(60)]
        sym_mat = spglib.get_symmetry(self._spg_cell, symprec=1e-4)
        ops = [(r,t) for r, t in zip(sym_mat['rotations'], sym_mat['translations'])]
        for r, t in ops:
            pos_new = np.transpose(np.matmul(r, np.transpose(self._positions))) + t
            perm = self._get_new_id_seq(pos_new, numbers)
            sym_perm.append(perm)

        return sym_perm

    @staticmethod
    def _get_new_id_seq(pos, numbers):
        """
        A helper function to produce the new sequence of the transformed 
        structure. Algs is sort the position back to init and use the index
        to sort numbers.
        """
        # transfer the atom position into >=0 and <=1
        pos = np.around(pos, decimals=5)
        func_tofrac = np.vectorize(lambda x: round((x % 1), 3))
        o_pos = func_tofrac(pos)
        # round_o_pos = np.around(o_pos, decimals=3)
        # z, y, x = round_o_pos[:, 2], round_o_pos[:, 1], round_o_pos[:, 0]
        z, y, x = o_pos[:, 2], o_pos[:, 1], o_pos[:, 0]
        inds = np.lexsort((z, y, x))

        return inds

    def get_name(self):
        """
        For the reason all structure have same lattice and positions
        only atom sequences are diff. Therefore as the hashable name
        and dict key.
        """
        return str(self._atom_numbers)

    def to_gen(self):
        """
        This a method convert a number seqents to a one element
        generator.
        """
        l = [self._atom_numbers]
        g = (n for n in l)
        return g

    @classmethod
    def gen_speckle(cls, sp, noa):
        """
        This method creates speckle structures which have speckles 
        number = noa.
        """
        i_sea = self._carbon.Z
        i_speckle = sp.Z
        for comb_index in combinations(range(60), noa):
            atom_numbers = [i_sea]*n
            for index in comb_index:
                atom_numbers[index] = i_speckle
            yield cls(atom_numbers)

    @staticmethod
    def help_add_one_speckle(l, sp):
        atom = sp.Z
        for index, val in enumerate(l):
            l_new= list(l)
            if val != atom:
                l_new[index] = atom
                yield l_new


    @staticmethod
    def add_one_speckle_generator(gen, sp):
        """
        input a structure generator(mostly nonduplicate)
        output a generator with one more speckle.
        This a method give duplicate structures which have one more speckle
        than the input structures.
        """
        atom = sp.Z
        idy_seq = set()
        for s_atoms in gen:
            for index, val in enumerate(s_atoms):
                l_new = list(s_atoms)
                if val != atom:
                    l_new[index] = atom
                    if str(l_new) not in idy_seq:
                        yield np.array(l_new)
                        idy_seq.add(str(l_new))

    @staticmethod
    def _get_atom_seq_identifier(numbers):
        """
        This method convert a list to a immutable string, which used
        as an identifier of diffrent structures, can be move to
        outerside class.
        """
        return str(list(numbers))

    def _update_isoset(self, isoset, atoms, sym_perm):
        for ind in sym_perm:
            print(atoms)
            print(ind)
            print(type(atoms))
            print(type(ind))
            print(len(atoms))
            atoms_new = atoms[ind]
            id_stru = self._get_atom_seq_identifier(atoms_new)
            isoset.add(id_stru)

        return isoset

    def to_nodup_generator(self, gen):
        """
        input: a generator with duplicate structures
        output: a generator with no structures dupicated
        This a method filter the duplicate structure to nonduplicates.
        """
        sym_perm = self.get_symmetry_permutation()

        isoset = set()
        for atoms in gen:
            id_stru = self._get_atom_seq_identifier(atoms)
            if id_stru not in isoset:
                yield atoms
                self._update_isoset(isoset, atoms, sym_perm)

    @staticmethod
    def all_speckle_gen(bucky_stru, n_max, sp):
        gen = bucky_stru.to_gen()
        n_init = bucky_stru.get_speckle_num(sp)
        for i in range(n_init, n_max+1):
            gen = add_one_speckle_generator(gen)
            gen = to_nodup_generator(gen)

        return gen

