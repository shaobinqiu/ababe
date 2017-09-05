# coding: utf-8
# Distributed under the terms of the MIT License.
import ababe
import sys
import click

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

@exec_from_cmdline.command()
def suplat(**kwargs):
    pass

@exec_from_cmdline.command()
def ocumaker(**kwargs):
    pass
