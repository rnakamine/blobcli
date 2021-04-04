import os

from azure.storage.blob import BlobServiceClient, BlobPrefix, BlobProperties


class BlobStorageClient():
    """Azure Blob Storage Client."""

    def __init__(self):
        connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
        if not connect_str:
            msg = 'Please add the connection string of the storage account to the AZURE_STORAGE_CONNECTION_STRING variable.'
            raise Exception(msg)

        self._blob_service_client = BlobServiceClient.from_connection_string(
            connect_str)

    def list_contaners(self):
        containers = [
            c for c in self._blob_service_client.list_containers() if not c.deleted]
        return containers

    def _convert_bytes(self, num):
        step_unit = 1024
        for x in ['B', 'K', 'M', 'G', 'T']:
            if num < step_unit:
                return '{:3.0f}{:s}'.format(num, x)
            num /= step_unit

    def list_blobs(self, container_name, blob_prefix):
        if container_name not in [c.name for c in self.list_contaners()]:
            msg = '{}: No such container'.format(container_name)
            raise Exception(msg)

        container_client = self._blob_service_client.get_container_client(
            container_name)

        blobs = []
        for blob in container_client.walk_blobs(name_starts_with=blob_prefix, delimiter='/'):
            if type(blob) == BlobPrefix:
                blobs.append({'name': blob.name,
                              'last_modified': None,
                              'size': 'PRE'})

            elif type(blob) == BlobProperties and not blob.deleted:
                blobs.append({'name': blob.name.split('/')[-1],
                              'last_modified': blob.last_modified,
                              'size': self._convert_bytes(blob.size)})

        if blob_prefix and not blobs:
            msg = '{}: No such blob'.format(blob_prefix)
            raise Exception(msg)

        return blobs

    def delete_blob(self, container_name, blob_name):
        blob_client = self._blob_service_client.get_blob_client(
            container_name, blob_name)

        if not blob_client.exists():
            msg = '{}/{}: No such container or blob'.format(
                container_name, blob_name)
            raise Exception(msg)

        blob_client.delete_blob()

    def upload_blob(self, container_name, blob_name, path):
        blob_client = self._blob_service_client.get_blob_client(
            container_name, blob=blob_name)

        with open(path, 'rb') as f:
            blob_client.upload_blob(f, overwrite=True)

    def copy_blob(self, src_container_name, src_blob_name, dst_container_name, dst_blob_name):
        src_blob_client = self._blob_service_client.get_blob_client(
            src_container_name, src_blob_name)
        dst_blob_client = self._blob_service_client.get_blob_client(
            dst_container_name, dst_blob_name)

        if not src_blob_client.exists():
            msg = '{}/{}: No such container or blob'.format(
                src_container_name, src_blob_name)
            raise Exception(msg)

        stream = src_blob_client.download_blob().readall()
        dst_blob_client.upload_blob(stream, overwrite=True)

    def download_blob(self, container_name, blob_name, path):
        blob_client = self._blob_service_client.get_blob_client(
            container_name, blob=blob_name)

        if not blob_client.exists():
            msg = '{}/{}: No such container or blob'.format(
                container_name, blob_name)
            raise Exception(msg)

        with open(path, 'wb') as f:
            f.write(blob_client.download_blob().readall())
