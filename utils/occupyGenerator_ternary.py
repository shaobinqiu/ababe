#!/usr/bin/env python

import argparse
import yaml
import tempfile
import shutil
import os
import numpy as np

from ababe.stru.sogen import OccupyGenerator
from ababe.stru.scaffold import GeneralCell
from ababe.stru.element import Specie
from ababe.stru.io import VaspPOSCAR
import pdb


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-fi', '--input', dest='settings',
            help='Setting file')
    parser.add_argument('-fo', '--output', dest='output_file',
            help='The location of output file')
    parser.add_argument('-s1', dest='sp1')
    parser.add_argument('-s2', dest='sp2')
    parser.add_argument('-n1', dest='n1')
    parser.add_argument('-n2', dest='n2')
    cmd_args = parser.parse_args()

    sp1 = cmd_args.sp1
    sp2 = cmd_args.sp2
    n1 = int(cmd_args.n1)
    n2 = int(cmd_args.n2)

    settings = open(cmd_args.settings, "r")
    args = yaml.load(settings)

    dir_name = args['comment']
    # lattice_dict = args['lattice']
    lattice = np.array(args['lattice'])
    positions = np.array(args['positions'])
    numbers = np.array(args['numbers'])
    # sp1 = args['sp1']
    # n1 = args['n1']
    # sp2 = args['sp2']
    # n2 = args['n2']
    zoom = args['zoom']
    # pdb.set_trace()

    # Write the structures into POSCARs dir
    working_path = os.getcwd()
    import random
    import string
    rd_suffix = ''.join(random.choices(string.ascii_uppercase
                                       + string.digits, k=4))
    working_path = os.getcwd()
    poscars_dir = os.path.join(working_path,
                               'POSCARs_{0:}_{1:}'.format(dir_name,
                                                          rd_suffix))
    # poscars_dir = os.path.join(working_path, 'POSCARs_{:}'.format(dir_name))
    if not os.path.exists(poscars_dir):
        os.makedirs(poscars_dir)
    else:
        shutil.rmtree(poscars_dir)
        os.makedirs(poscars_dir)

    cell = GeneralCell(lattice, positions, numbers)
    ogg = OccupyGenerator(cell)
    gg = ogg.gen_nodup_trinary_alloy(Specie(sp1), n1, Specie(sp2), n2)

    for c in gg:
        if c.is_primitive():
            poscar = VaspPOSCAR(c.spg_cell, zoom)
            tf = tempfile.NamedTemporaryFile(mode='w+b', dir=poscars_dir,
                    prefix='POSCAR_S_', suffix='.vasp', delete=False)
            poscar.write_POSCAR(tf.name)


if __name__ == "__main__":
    main()


