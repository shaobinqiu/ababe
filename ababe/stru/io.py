# coding: utf-8
# Distributed under the terms of the MIT License.

class VaspPOSCAR(Object):

    def __init__(self, cstru):
        self.structure = cstru.copy()

    def get_string(self, direct=True):
        """
        Returns:
            String represention of POSCAR.
        """
        latt = self.lattice

        lines = ["none", "1.0", str(latt)]
        lines.append("")    # number of atoms
        lines.append("direct" if direct else "cartesian")


    def __repr__(self):
        return self.get_string()

    def __str__(self):
        """
        String representation of Poscar file
        """
        return self.get_string()

    def write_POSCAR(self, filename):
        """
        Writes POSCAR to a file.
        """
        pass
