#!/usr/bin/env python
import argparse
import yaml
import tempfile
import shutil

# sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
# from ababe.stru.scaffold import CStru
from ababe.stru.element import Specie
from ababe.stru.sogen import gen_nodup_cstru, is_speckle_disjunct, lat_dict
from ababe.stru.io import VaspPOSCAR
import os


def default(str):
    return str + '  [Default: %(default)s]'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-fi', '--input', dest='settings',
                            help='Setting file for site-occupied generator')
    parser.add_argument('-fo', '--output', dest='output_file',
                            help='The location of output file')
    cmd_args = parser.parse_args()

    settings = open(cmd_args.settings, "r")
    args = yaml.load(settings)
    # print(args)

    size = args['grid_size']
    sea_ele = Specie(args['base'])
    speckle = Specie(args['speckle'])

    nodup_gen = gen_nodup_cstru(lat_dict(args['lattice']), sea_ele, size, speckle, args['number'])

    if args["restriction"]:
        result = list(filter(lambda x: is_speckle_disjunct(x, speckle), nodup_gen))
        # print(result)
        # result = []
        # for c in nodup_gen:
        #     # print(c)
        #     print(is_speckle_disjunct(c, speckle))

        #     if is_speckle_disjunct(c, speckle):
        #         # print(is_speckle_disjunct(c, speckle))
        #         result.append(c)

        # print(result)
    else:
        result = list(nodup_gen)

    with open(cmd_args.output_file, 'w') as f:
        print("\n\nThere are {0} structures nonduplicated.".format(len(result)))
        f.write('#######################################################\n')
        f.write('There are {0} structures nonduplicated\n'.format(len(result)))
        f.write('#######################################################')
        f.write('\n\n')

        for s in result:
            # print(result)
            basis, pos, atom = s.get_cell()
            f.write('ONE NEW STRUCTURE:\n')
            f.write('The basis is:\n')
            f.write('\n'.join(str(line) for line in basis))

            f.write('\nThe position is:\n')
            f.write('\n'.join(str(line) for line in pos))

            f.write('\nThe elements is:\n')
            f.write(str(atom))

            f.write('\nThe array is:\n')
            f.write('\n'.join(str(line) for line in s.get_array()))

            f.write('\n\n\n')

    # Write the structures into POSCARs dir
    working_path = os.getcwd()
    poscars_dir = os.path.join(working_path, 'POSCARs')
    if not os.path.exists(poscars_dir):
        os.makedirs(poscars_dir)
    else:
        shutil.rmtree(poscars_dir)
        os.makedirs(poscars_dir)

    for s in result:
        working_poscar = VaspPOSCAR(s.get_cell())
        tf = tempfile.NamedTemporaryFile(mode='w+b', dir=poscars_dir,
                                                prefix='POSCAR_', suffix='.vasp', delete=False)
        working_poscar.write_POSCAR(tf.name)


if __name__ == "__main__":
    main()