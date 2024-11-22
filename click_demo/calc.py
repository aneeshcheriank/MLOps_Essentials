#!/usr/bin/env python
"""
This module is to demonstrate the caipabilities of click
"""

import click

def add(x, y):
    return x+y

def subtract(x, y):
    return x-y

@click.group()
def cli():
    """This is a calculator app"""

@cli.command('add')
@click.argument('x', type=int)
@click.argument('y', type=int)
def add_command(x, y):
    """
    This function adds two numbers
    """
    click.echo(add(x, y))

@cli.command('subtract')
@click.argument('x', type=int)
@click.argument('y', type=int)
def subtract_command(x, y):
    """
    This function subtract two numbers
    """
    click.echo(subtract(x, y))

if __name__ == '__main__':
    cli()

