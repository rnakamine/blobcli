import json
import sys

import click

from .client import BlobStorageClient


@click.group()
def cli():
    pass


@cli.command(help='List containers or blobs.')
@click.argument('target', default='')
def ls(target):
    """List containers or blobs."""
    blob_client = BlobStorageClient()
    if target:
        blobs = blob_client.list_blobs(target)
        for blob in blobs:
            click.echo('{:>25} {:>5} {}'.format(
                str(blob['last_modified'] or ''), blob['size'] or '', blob['name']))
    else:
        containers = blob_client.list_contaners()
        for container in containers:
            click.echo('{} {}'.format(
                container['last_modified'], container['name']))


@cli.command(help='Delete blob.')
@click.argument('target')
def rm(target):
    """Delete blob."""
    output = BlobStorageClient().delete_blob(target)
    click.echo(output)


@cli.command(help='Copy blob.')
@click.argument('src')
@click.argument('dst')
def cp(src, dst):
    """Copy blob."""
    output = BlobStorageClient().transfer_blob(src, dst, delete_flag=False)
    click.echo(output)


@cli.command(help='Move blob.')
@click.argument('src')
@click.argument('dst')
def mv(src, dst):
    """Move blob."""
    output = BlobStorageClient().transfer_blob(src, dst, delete_flag=True)
    click.echo(output)


def main():
    try:
        cli()
        sys.exit(0)
    except Exception as e:
        click.echo(e, err=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
