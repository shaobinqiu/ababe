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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-fi', '--input', dest='settings',
                        help='Setting file')
    # parser.add_argument('-fo', '--output', dest='output_file',
    #                     help='The location of output file')
    parser.add_argument('-e', '--element', dest='element',
                        help='which element species to be replaced.')
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
        nmax = math.ceil(numbers.size/2)  # default half+1 number of speckles

    ele = Specie(cmd_args.element)

    # Write the structures into POSCARs dir
    import random
    import string
    rd_suffix = ''.join(random.choices(string.ascii_uppercase
                                       + string.digits, k=4))
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
    gg = ogg.all_speckle_gen_of_ele(nmax, ele, Specie(speckle))
    # pdb.set_trace()

    print("Mission: Replace with {0:3}, up to number \
          {1:3d}...".format(speckle, nmax))
    for i, outer_gen in enumerate(gg):
        print("Processing: {0:3}s substitue {1:2d}...".format(speckle, i+1))
        for n_count, c in enumerate(outer_gen):
            if c.is_primitive():
                poscar = VaspPOSCAR(c.spg_cell, zoom)
                tf = tempfile.NamedTemporaryFile(mode='w+b', dir=poscars_dir,
                                                 prefix='POSCAR_S{:}_'
                                                        .format(i+1),
                                                 suffix='.vasp', delete=False)
                poscar.write_POSCAR(tf.name)
        # pdb.set_trace()
        # print("Total {0:3d} nonduplicated structures in {1:3d} \
        #       substitute.".format(n_count+1, i+1))


if __name__ == "__main__":
    main()
