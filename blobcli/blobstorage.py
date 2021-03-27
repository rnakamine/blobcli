import os
import sys

import click
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient


class BlobStorage():

    def __init__(self):
        self._blob_service_client = BlobServiceClient.from_connection_string(
            os.getenv('AZURE_STORAGE_CONNECTION_STRING'))

    def list_contaners(self):
        containers = self._blob_service_client.list_containers()
        return containers

    def list_blobs(self, target):
        if not target.startswith('blob://'):
            click.echo('ls: {}: Invalid target'.format(target), err=True)
            sys.exit(1)

        original_target = target
        if target.endswith('/'):
            target = target[:-1]

        target = target.replace('blob://', '').split('/')
        container_name = target[0]
        target_path_list = target[1:]

        container_client = self._blob_service_client.get_container_client(
            container_name)

        blobs = []
        tmp_dir_name = []
        for blob in container_client.list_blobs():
            if not blob.deleted:
                blob_path_list = blob.name.split('/')
                if target_path_list:
                    if self._find_blob(target_path_list, blob_path_list):
                        if target_path_list == blob_path_list:
                            blob_path_list = blob_path_list[-1:]
                        else:
                            blob_path_list = blob_path_list[len(
                                target_path_list):]
                    else:
                        continue

                name, last_modified, size = None, None, None

                # check directory or file
                if len(blob_path_list) > 1:
                    if blob_path_list[0] not in tmp_dir_name:
                        name = blob_path_list[0] + '/'
                        tmp_dir_name.append(blob_path_list[0])
                else:
                    name = blob_path_list[0]
                    last_modified = blob.last_modified
                    size = blob.size

                blobs.append(
                    {'name': name, 'last_modified': last_modified, 'size': size})

        if not blobs:
            click.echo('ls: {}: No such blob or directory'.format(
                original_target), err=True)
            sys.exit(1)

        return blobs

    def _find_blob(self, target_path_list, blob_path_list):
        for i, t in enumerate(target_path_list):
            if t != blob_path_list[i]:
                return False
        return True
