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
    cmd_args = parser.parse_args()

    settings = open(cmd_args.settings, "r")
    args = yaml.load(settings)

    dir_name = args['comment']
    # lattice_dict = args['lattice']
    lattice = np.array(args['lattice'])
    positions = np.array(args['positions'])
    numbers = np.array(args['numbers'])
    speckle = args['speckle']
    nmax = args['n']
    pdb.set_trace()

    # Write the structures into POSCARs dir
    working_path = os.getcwd()
    poscars_dir = os.path.join(working_path, 'POSCARs_{:}'.format(dir_name))
    if not os.path.exists(poscars_dir):
        os.makedirs(poscars_dir)
    else:
        shutil.rmtree(poscars_dir)
        os.makedirs(poscars_dir)

    cell = GeneralCell(lattice, positions, numbers)
    ogg = OccupyGenerator(cell)
    gg = ogg.all_speckle_gen(nmax, Specie(speckle))

    print("Mission: Replace with {0:3}, up to number {1:3d}...".format(speckle, nmax))
    for i, outer_gen in enumerate(gg):
        print("Processing: {0:3}s substitue {1:2d}...".format(speckle, i+1))
        for n_count, c in enumerate(outer_gen):
            poscar = VaspPOSCAR(c.spg_cell)
            tf = tempfile.NamedTemporaryFile(mode='w+b', dir=poscars_dir,
                    prefix='POSCAR_S{:}_'.format(i+1), suffix='.vasp', delete=False)
            poscar.write_POSCAR(tf.name)
        print("Total {0:3d} nonduplicated structures in {1:3d} substitute.".format(n_count+1, i+1))


if __name__ == "__main__":
    main()


