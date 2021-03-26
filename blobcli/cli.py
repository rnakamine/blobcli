import json

import click

import blobstorage


@click.group()
def cli():
    pass


@cli.command()
@click.argument('target', default='')
def ls(target):
    """List containers or blobs."""
    if target:
        obj = blobstorage.list_blobs(target)
    else:
        obj = blobstorage.list_contaners()

    for o in obj:
        click.echo('{}\t{}'.format(o['last_modified'], o['name']))


if __name__ == '__main__':
    cli()
