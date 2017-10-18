# coding: utf-8
# Distributed under the terms of the MIT License.
import ababe
import click
import sys, ast
import yaml
from ababe.cmdline.apps import *

def run():
    try:
        ababe.cmdline.runatilib.exec_from_cmdline()
    except KeyboardInterrupt:
        pass
    except EOFError:
        pass

@click.group()
@click.version_option(version='0.1.0')
def exec_from_cmdline():
    pass

@exec_from_cmdline.command()
@click.argument('input', type=click.Path(exists=True))
@click.option('--center-element', '-c', 'cenele', required=True)
@click.option('--radius', '-r', type=float, default=0)
@click.option('--element-remove', '-e', 'ele', required=True)
@click.option('--refined/--no-refined', default=True)
def atclear(input, cenele, radius, ele, refined):
    infile = click.format_filename(input)
    filename = infile
    y = yaml.load(open(infile, "r"))

    appatomclarifier = atomclarifier.App(y, filename, cenele, radius, ele, refined)
    appatomclarifier.run()
    
@exec_from_cmdline.command()
@click.argument('input', type=click.Path(exists=True))
@click.option('--scale-matrix', prompt=True)
@click.option('--zoom', type=float, default=None)
@click.option('--outmode', type=click.Choice(['vasp', 'yaml']), default='yaml')
def supcell(input, scale_matrix, zoom, outmode):
    infile = click.format_filename(input)
    y = yaml.load(open(infile, "r"))

    l = ast.literal_eval(scale_matrix)
    appsupercell = supercell.App(y, l, zoom, outmode)
    appsupercell.run()

@exec_from_cmdline.command()
@click.argument('input', type=click.Path(exists=True))
@click.option('--outmode', type=click.Choice(['vasp', 'yaml']), default='yaml')
def pcell(input, outmode):
    infile = click.format_filename(input)
    settings = yaml.load(open(infile, "r"))

    from ababe.stru.scaffold import GeneralCell
    from ababe.stru.sogen import OccupyGenerator
    from ababe.stru.io import VaspPOSCAR, YamlOutput
    import numpy as np

    lat = np.array(settings['lattice'])
    pos = np.array(settings['positions'])
    num = np.array(settings['numbers'])
    cell = GeneralCell(lat, pos, num)
    pcell = cell.get_refined_pcell()
    if outmode == 'yaml':
        beprint = YamlOutput(pcell, 1)
    elif outmode == 'vasp':
        beprint = VaspPOSCAR(pcell, 1)

    print(beprint)
