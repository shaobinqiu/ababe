# coding: utf-8
# Distributed under the terms of the MIT License.

from ababe.stru.element import Specie

class VaspPOSCAR(object):

    def __init__(self, cstru):
        self.structure = cstru
        self.lattice = cstru.get_lattice()
        self.positions = cstru.get_positions()
        self.atoms = cstru.get_atoms()

        self.atoms_name_list = list(map(lambda x: Specie.to_name(x), list(self.atoms)))

    def get_string(self, direct=True):
        """
        Returns:
            String represention of POSCAR.
        """
        from collections import Counter, OrderedDict
        from operator import itemgetter

        latt = self.lattice
        d = Counter(self.atoms_name_list)
        orderd_atoms = OrderedDict(sorted(d.items(), key=lambda x: Specie(x[0]).Z))
        if 'G' in orderd_atoms:
            del orderd_atoms['G']

        comment = ''.join(['{}{}'.format(k,v) for k,v in orderd_atoms.items()])

        lines = [comment, "1.0"]
        # lattice string
        for c in self.lattice:
            line = " ".join("{:10.6f}".format(p) for p in c)
            lines.append(line)

        

        lines.append(" ".join([str(x) for x in orderd_atoms.keys()]))
        lines.append(" ".join([str(x) for x in orderd_atoms.values()]))

        zipped_list = list(zip(self.atoms, self.positions, self.atoms_name_list))
        sorted_position = sorted(zipped_list, key=itemgetter(0))

        lines.append("direct" if direct else "cartesian")

        # sort the positions by atoms seqence
        
        for (i, pos, site) in sorted_position:
            if not i == 0:
                line = " ".join(["{:10.6f}".format(p) for p in pos]) 
                line += " " + site
                lines.append(line)

        return "\n".join(lines) + "\n"       


    def __repr__(self):
        return self.get_string()

    def __str__(self):
        """
        String representation of Poscar file
        """
        print(self.get_string())
        return self.get_string()

    def write_POSCAR(self, filename):
        """
        Writes POSCAR to a file.
        """
        with open(filename, "w") as f:
            f.write(self.get_string())
