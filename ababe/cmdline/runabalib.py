# coding: utf-8
# Distributed under the terms of the MIT License.
import ababe
import sys, ast
import click
import yaml
from ababe.cmdline.apps import *

def run():
    try:
        ababe.cmdline.runabalib.exec_from_cmdline()
    except KeyboardInterrupt:
        pass
    except EOFError:
        pass

@click.group()
@click.version_option(version='0.1.0')
def exec_from_cmdline():
    pass

#######################################################################
## In the module all inputs from cmd-line is checked
## And then call the modules in directory
## ababe/cmdline/command
#######################################################################
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
@click.option('--comment', default=None)
@click.option('--volumn', type=int, default=1)
@click.option('--zoom', type=float, default=None)
@click.option('--ld/--no-ld', '-L/', default=False)
@click.option('--outmode', type=click.Choice(['vasp', 'yaml']), default='yaml')
def suplat(input, comment, volumn, zoom, ld, outmode):
    infile = click.format_filename(input)
    y = yaml.load(open(infile, "r"))

    appsuperlattice = superlattice.App(y, comment, volumn, zoom, ld, outmode)
    appsuperlattice.run()

@exec_from_cmdline.command()
@click.argument('input', type=click.Path(exists=True))
@click.option('--comment', default=None)
@click.option('--element', default=None)
@click.option('--speckle', default=None)
@click.option('--number-speckle', '-n', 'nspeckle', type=int, default=None)
@click.option('--zoom', type=float, default=None)
@click.option('--dist-restrict', '-r', 'trs', nargs=2, type=click.Tuple([str, float]), multiple=True)
@click.option('--outmode', type=click.Choice(['vasp', 'yaml']), default='vasp')
def ocumaker(input, comment, element, speckle, nspeckle, zoom, trs, outmode):
    infile = click.format_filename(input)
    y = yaml.load(open(infile, "r"))

    appoccupymaker = occupymaker.App(y, comment, element, speckle, nspeckle, zoom, trs, outmode)
    appoccupymaker.run()

@exec_from_cmdline.command()
@click.argument('input', type=click.Path(exists=True))
@click.option('--center-element', '-c', 'cenele', required=True)
@click.option('--radius', '-r', default=0)
@click.option('--element-remove', '-e', 'ele', required=True)
def atclear(input, cenele, radius, ele):
    infile = click.format_filename(input)
    filename = infile
    y = yaml.load(open(infile, "r"))

    appatomclarifier = atomclarifier.App(y, filename, cenele, radius, ele)
    appatomclarifier.run()
