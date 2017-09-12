# coding: utf-8
# Distributed under the terms of the MIT License.
import ababe
import sys, ast
import click
import yaml
from ababe.cmdline.apps import supercell

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
@click.option('--zoom', default=1)
@click.option('--outmode', default='yaml')
def supcell(input, scale_matrix, zoom, outmode):
    infile = click.format_filename(input)
    y = yaml.load(open(infile, "r"))

    l = ast.literal_eval(scale_matrix)
    z = zoom
    appsupercell = supercell.App(y, l, z)
    appsupercell.run(outmode)

@exec_from_cmdline.command()
def suplat(**kwargs):
    pass

@exec_from_cmdline.command()
def ocumaker(**kwargs):
    pass
