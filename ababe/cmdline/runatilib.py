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

    appatomclarifier = atomclarifier.App(infile, cenele, radius, ele, refined)
    appatomclarifier.run()

@exec_from_cmdline.command()
@click.argument('input', type=click.Path(exists=True))
@click.option('--radius', '-r', type=float, default=0)
def perturb(input, radius):
    infile = click.format_filename(input)

    appperturb = atomperturb.App(infile, radius)
    appperturb.run()

@exec_from_cmdline.command()
@click.argument('input', type=click.Path(exists=True))
@click.option('--scale', '-s', nargs=3, type=int)
@click.option('--outmode', type=click.Choice(['vasp', 'yaml', 'stdio']), default='stdio')
def supcell(input, scale, outmode):
    from ababe.io.io import GeneralIO
    import os
    import numpy as np

    infile = click.format_filename(input)
    basefname = os.path.basename(infile)

    gcell = GeneralIO.from_file(infile)

    scale_matrix = np.diag(np.array(scale))
    sc = gcell.supercell(scale_matrix)

    out = GeneralIO(sc)

    print("PROCESSING: {:}".format(infile))
    if outmode == 'stdio':
        out.write_file(fname=None, fmt='vasp')
    else:
        ofname = "{:}_SUPC.{:}".format(basefname.split('.')[0], outmode)
        out.write_file(ofname)

@exec_from_cmdline.command()
@click.argument('input', type=click.Path(exists=True))
@click.option('--outmode', type=click.Choice(['vasp', 'yaml', 'stdio']), default='stdio')
def pcell(input, outmode):
    from ababe.io.io import GeneralIO
    import os
    infile = click.format_filename(input)
    basefname = os.path.basename(infile)

    gcell = GeneralIO.from_file(infile)
    pcell = gcell.get_refined_pcell()

    out = GeneralIO(pcell)

    if outmode == 'stdio':
        out.write_file(fname=None, fmt='vasp')
    else:
        print("PROCESSING: {:}".format(infile))
        ofname = "{:}_PRIMC.{:}".format(basefname.split('.')[0], outmode)
        out.write_file(ofname)
