import json

import click

from .blobstorage import BlobStorage


@click.group()
def cli():
    pass


@cli.command()
@click.argument('target', default='')
def ls(target):
    """List containers or blobs."""
    blobstorage = BlobStorage()
    if target:
        blobs = blobstorage.list_blobs(target)
        for blob in blobs:
            click.echo('{}\t{} {}'.format(
                blob['last_modified'] or '', blob['size'] or '', blob['name']))
    else:
        containers = blobstorage.list_contaners()
        for container in containers:
            click.echo('{}\t{}'.format(
                container['last_modified'], container['name']))


if __name__ == '__main__':
    cli()
