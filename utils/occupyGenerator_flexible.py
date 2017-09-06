#!/usr/bin/env python

import argparse
import yaml
import tempfile
import shutil
import os
import numpy as np
import math

from ababe.stru.sogen import OccupyGenerator
from ababe.stru.scaffold import GeneralCell
from ababe.stru.element import Specie
from ababe.stru.io import VaspPOSCAR
# import pdb


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-fi', '--input', dest='settings',
                        help='Setting file')
    # parser.add_argument('-fo', '--output', dest='output_file',
    #                     help='The location of output file')
    parser.add_argument('-w', '--wyckoff-site', dest='wyckoff',
                        help='which wyckoff site to be replaced.')
    parser.add_argument('-s', '--speckle-element', dest='speckle',
                        help='substitute with what element.')
    parser.add_argument('-n', '--number-speckle', dest='nmax', type=int,
                        help='the max number of speckles to be replaced.')

    cmd_args = parser.parse_args()

    # parameters read from yaml file
    settings = open(cmd_args.settings, "r")
    args = yaml.load(settings)
    dir_name = args['comment']
    lattice = np.array(args['lattice'])
    positions = np.array(args['positions'])
    numbers = np.array(args['numbers'])
    zoom = args['zoom']

    # parameters read from command line
    speckle = cmd_args.speckle
    if cmd_args.nmax is not None:
        nmax = cmd_args.nmax
    else:
        nmax = numbers.size  # default half+1 number of speckles

    wy = cmd_args.wyckoff
    # pdb.set_trace()

    # Write the structures into POSCARs dir
    import random
    import string
    rd_suffix = ''.join(random.choices(string.ascii_uppercase
                                       + string.digits, k=5))
    working_path = os.getcwd()
    poscars_dir = os.path.join(working_path,
                               'POSCARs_{0:}_{1:}'.format(dir_name,
                                                          rd_suffix))
    if not os.path.exists(poscars_dir):
        os.makedirs(poscars_dir)
    else:
        shutil.rmtree(poscars_dir)
        os.makedirs(poscars_dir)

    cell = GeneralCell(lattice, positions, numbers)
    ogg = OccupyGenerator(cell)
    gg = ogg.all_speckle_gen(nmax, wy, Specie(speckle))
    # pdb.set_trace()

    for i, outer_gen in enumerate(gg):
        for n_count, c in enumerate(outer_gen):
            if c.is_primitive():
                c = c.get_refined_pcell()
                poscar = VaspPOSCAR(c.spg_cell, zoom)
                tf = tempfile.NamedTemporaryFile(mode='w+b', dir=poscars_dir,
                                                 prefix='POSCAR_S{:}_'
                                                        .format(i+1),
                                                 suffix='.vasp', delete=False)
                poscar.write_POSCAR(tf.name)
        # pdb.set_trace()


if __name__ == "__main__":
    main()
