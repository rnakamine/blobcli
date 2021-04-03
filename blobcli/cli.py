import json
import os
import sys

import click

from .client import BlobStorageClient


def _extract_container_name(path):
    container_name = path.split('/')[0]
    path = '/'.join(path.split('/')[1:])
    if not path:
        path = None
    return container_name, path


def blob_storage_to_blob_storage(src, dst, delete_flag=False):
    src = src.replace('blob://', '')
    dst = dst.replace('blob://', '')
    src_container_name, src_blob_name = _extract_container_name(
        src)
    dst_container_name, dst_blob_path = _extract_container_name(
        dst)

    if dst_blob_path:
        if dst_blob_path.endswith('/'):
            dst_blob_name = os.path.join(
                dst_blob_path, os.path.basename(src_blob_name))
        else:
            dst_blob_name = dst_blob_path
    else:
        dst_blob_name = os.path.basename(src_blob_name)

    BlobStorageClient().upload_blob_from_blob_storage(
        src_container_name, src_blob_name, dst_container_name, dst_blob_name)
    if delete_flag:
        BlobStorageClient().delete_blob(src_container_name, src_blob_name)


def blob_storage_to_local(src, dst, delete_flag=False):
    src = src.replace('blob://', '')
    container_name, blob_name = _extract_container_name(src)

    if dst.endswith('/') or dst == '.':
        dst = os.path.join(dst, os.path.basename(blob_name))

    BlobStorageClient().download_blob(container_name, blob_name, dst)
    if delete_flag:
        BlobStorageClient().delete_blob(container_name, blob_name)


def local_to_blob_storage(src, dst, delete_flag=False):
    dst = dst.replace('blob://', '')
    container_name, dst_path = _extract_container_name(dst)

    if dst_path:
        if dst.endswith('/'):
            blob_name = os.path.join(os.path.dirname(
                dst_path), os.path.basename(src))
        else:
            blob_name = dst_path
    else:
        blob_name = os.path.basename(src)

    BlobStorageClient().upload_blob(container_name, blob_name, src)
    if delete_flag:
        os.remove(src)


@click.group()
def cli():
    pass


@cli.command(help='List containers or blobs.')
@click.argument('target', default='')
def ls(target):
    """List containers or blobs."""
    blob_client = BlobStorageClient()
    if target:
        if target.startswith('blob://'):
            target = target.replace('blob://', '')
        container_name, blob_prefix = _extract_container_name(target)
        blobs = blob_client.list_blobs(container_name, blob_prefix)
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
    original_target = target
    if target.startswith('blob://'):
        target = target.replace('blob://', '')
    else:
        msg = 'rm: Invalid argument type'
        raise Exception(msg)
    container_name, blob_name = _extract_container_name(target)
    BlobStorageClient().delete_blob(container_name, blob_name)

    click.echo('delete: {}'.format(original_target))


@cli.command(help='Copy blob.')
@click.argument('src')
@click.argument('dst')
def cp(src, dst):
    """Copy blob."""
    original_src, original_dst = src, dst
    if src.startswith('blob://') and dst.startswith('blob://'):
        blob_storage_to_blob_storage(src, dst, delete_flag=False)
    elif src.startswith('blob://'):
        blob_storage_to_local(src, dst, delete_flag=False)
    elif dst.startswith('blob://'):
        local_to_blob_storage(src, dst, delete_flag=False)

    click.echo('copy: {} to {}'.format(original_src, original_dst))


@cli.command(help='Move blob.')
@click.argument('src')
@click.argument('dst')
def mv(src, dst):
    """Move blob."""
    original_src, original_dst = src, dst
    if src.startswith('blob://') and dst.startswith('blob://'):
        blob_storage_to_blob_storage(src, dst, delete_flag=True)
    elif src.startswith('blob://'):
        blob_storage_to_local(src, dst, delete_flag=True)
    elif dst.startswith('blob://'):
        local_to_blob_storage(src, dst, delete_flag=True)

    click.echo('move: {} to {}'.format(original_src, original_dst))


def main():
    try:
        cli()
        sys.exit(0)
    except Exception as e:
        click.echo(e, err=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
