#!/usr/bin/env python
import argparse
import sys
import os.path

def lat_dict(lattice):
    lat = { 'tri': [[1.0, 0.0],
                    [0.5, 0.866]]}

def default(str):
    return str + '  [Default: %(default)s]'

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--lattice', choices=['tri'],
                            help='Lattice type of grid 2d conventional cell')
    parser.add_argument('-b', '--base', dest='sea', required=True,
                            help='Element abbreviation of the base specie')
    parser.add_argument('-g', '--size', nargs=2, dest='size', required=True,
                            help='Grid size of 2d structure', type=int)
    parser.add_argument('-s', '--speckle', dest='speckle', required=True,
                            help='Element abbreviation of the speckle specie')
    parser.add_argument('-n', '--num', dest='number', type=int, 
                            help=default('Number of speckles filled in the base'), default=2)
    parser.add_argument('-o', '--output-type', 
                            help=default('Output type of generated non-duplicate periodic grid sturcture'),
                                default='normal')

    args = parser.parse_args()
    size = args.size
    sea_ele = Specie(args.sea)
    speckle = Specie(args.speckle)

    nodup_gen = gen_nodup_cstru(lat_dict(args.lattice), sea_ele, size, speckle, args.number)
    with open('allstru.txt', 'w') as f:
        for s in nodup_gen:
            basis, pos, atom = s.get_cell()
            f.write('ONE NEW STRUCTURE:\n')
            f.write('The basis is:\n')
            f.write('\n'.join(str(line) for line in basis))

            f.write('\nThe position is:\n')
            f.write('\n'.join(str(line) for line in pos))

            f.write('\nThe elements is:\n')
            f.write(str(atom))

            f.write('\n\n\n')


if __name__ == "__main__"
    main()