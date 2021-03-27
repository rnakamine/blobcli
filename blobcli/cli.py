import json

import click

from .client import BlobStorageClient


@click.group()
def cli():
    pass


@cli.command()
@click.argument('target', default='')
def ls(target):
    """List containers or blobs."""

    blob_client = BlobStorageClient()
    if target:
        blobs = blob_client.list_blobs(target)
        for blob in blobs:
            click.echo('{}\t{} {}'.format(
                blob['last_modified'] or '', blob['size'] or '', blob['name']))
    else:
        containers = blob_client.list_contaners()
        for container in containers:
            click.echo('{}\t{}'.format(
                container['last_modified'], container['name']))


if __name__ == '__main__':
    cli()
