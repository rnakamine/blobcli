import os

from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient


class BlobStorageClient():

    def __init__(self):
        self._blob_service_client = BlobServiceClient.from_connection_string(
            os.getenv('AZURE_STORAGE_CONNECTION_STRING'))

    def list_contaners(self):
        containers = self._blob_service_client.list_containers()
        return containers

    def list_blobs(self, target):
        if not target.startswith('blob://'):
            msg = 'ls: {}: Invalid target'.format(target)
            raise Exception(msg)

        original_target = target
        if target.endswith('/'):
            target = target[:-1]

        target = target.replace('blob://', '').split('/')
        container_name = target[0]
        target_path_list = target[1:]

        container_client = self._blob_service_client.get_container_client(
            container_name)
        list_blobs = [b for b in container_client.list_blobs()
                      if not b.deleted]

        blobs, dirs = [], []
        tmp_dir_name = []
        for blob in list_blobs:
            blob_path_list = blob.name.split('/')
            if target_path_list:
                if self._find_blob(target_path_list, blob_path_list):
                    if target_path_list == blob_path_list:
                        blob_path_list = blob_path_list[-1:]
                    else:
                        blob_path_list = blob_path_list[len(target_path_list):]
                else:
                    continue

            # check directory or file
            if len(blob_path_list) > 1:  # when directory
                if blob_path_list[0] not in tmp_dir_name:
                    dirs.append({'name': blob_path_list[0] + '/',
                                 'last_modified': None,
                                 'size': 'PRE'})
                    tmp_dir_name.append(blob_path_list[0])
            else:  # when blob
                blobs.append({'name': blob_path_list[0],
                              'last_modified': blob.last_modified,
                              'size': self._convert_bytes(blob.size)})

        blobs = dirs + blobs
        if not blobs:
            msg = 'ls: {}: No such blob or directory'.format(original_target)
            raise Exception(msg)

        return blobs

    def _find_blob(self, target_path_list, blob_path_list):
        for i, t in enumerate(target_path_list):
            if t != blob_path_list[i]:
                return False
        return True

    def _convert_bytes(self, num):
        step_unit = 1024
        for x in ['B', 'K', 'M', 'G', 'T']:
            if num < step_unit:
                return '{:3.0f}{:s}'.format(num, x)
            num /= step_unit
