#!/usr/bin/env python

import argparse
import yaml
import tempfile
import shutil
import os
import numpy as np

from ababe.stru.grid import SuperLatticeGenerator
from ababe.stru.io import VaspPOSCAR, YamlOutput
# import pdb


def print_POSCARs(dir_name, volumn_max, unit_cell, zoom):
    for v in range(1, volumn_max+1):
        hnfs = SuperLatticeGenerator.hnfs_from_n(unit_cell, v)
        for hnf in hnfs:
            sl = hnf.to_general_cell()
            poscar = VaspPOSCAR(sl.spg_cell, zoom)
            # pdb.set_trace()
            tf = tempfile.NamedTemporaryFile(mode='w+b', dir=dir_name,
                                             prefix='SUPERLATT_S{:}_'.
                                             format(v),
                                             suffix='.vasp', delete=False)
            poscar.write_POSCAR(tf.name)


def print_YAML(dir_name, volumn_max, unit_cell, zoom):
    for v in range(1, volumn_max+1):
        hnfs = SuperLatticeGenerator.hnfs_from_n(unit_cell, v)
        for hnf in hnfs:
            sl = hnf.to_general_cell()
            yml = YamlOutput(sl.spg_cell, zoom)
            # pdb.set_trace()
            tf = tempfile.NamedTemporaryFile(mode='w+b', dir=dir_name,
                                             prefix='SUPERLATT_S{:}_'.
                                             format(v),
                                             suffix='.yaml', delete=False)
            yml.write_YAML(tf.name)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-fi', '--input', dest='settings',
                        help='Setting file')
    # parser.add_argument('-fo', '--output', dest='output_file',
    #         help='The location of output file')
    cmd_args = parser.parse_args()

    settings = open(cmd_args.settings, "r")
    args = yaml.load(settings)

    dir_name = args['comment']
    unit_basis = np.array(args['unit_basis'])
    unit_positions = np.array(args['unit_positions'])
    unit_numbers = np.array(args['unit_numbers'])
    volumn_max = args['volumn']
    zoom = args['zoom']
    outtype = args['outfile_type']
    # pdb.set_trace()

    # Write the structures into OUTPUTs dir
    working_path = os.getcwd()
    superlattice_dir = os.path.join(working_path,
                                    'SUPERLATTs_{:}'.format(dir_name))
    if not os.path.exists(superlattice_dir):
        os.makedirs(superlattice_dir)
    else:
        shutil.rmtree(superlattice_dir)
        os.makedirs(superlattice_dir)

    unit_cell = (unit_basis, unit_positions, unit_numbers)
    # pdb.set_trace()
    if outtype == 'vasp':
        print_POSCARs(superlattice_dir, volumn_max, unit_cell, zoom)
    else:
        # print("TO BE CONTINUE...")
        print_YAML(superlattice_dir, volumn_max, unit_cell, zoom)


if __name__ == "__main__":
    main()
