import os

from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, BlobPrefix, BlobProperties


class BlobStorageClient():

    def __init__(self):
        connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
        if not connect_str:
            msg = 'Please add the connection string of the storage account to the AZURE_STORAGE_CONNECTION_STRING variable.'
            raise Exception(msg)

        self._blob_service_client = BlobServiceClient.from_connection_string(
            connect_str)

    def list_contaners(self):
        list_containers = [
            c for c in self._blob_service_client.list_containers() if not c.deleted]
        return list_containers

    def list_blobs(self, target):
        original_target = target

        if target.startswith('blob://'):
            target = target.replace('blob://', '')

        container_name = target.split('/')[0]
        target_path = '/'.join(target.split('/')[1:])

        if container_name not in [c.name for c in self.list_contaners()]:
            msg = 'ls: {}: No such container'.format(original_target)
            raise Exception(msg)

        container_client = self._blob_service_client.get_container_client(
            container_name)

        blobs = []
        for blob in container_client.walk_blobs(name_starts_with=target_path, delimiter='/'):
            if type(blob) == BlobPrefix:
                blobs.append({'name': blob.name,
                              'last_modified': None,
                              'size': 'PRE'})

            elif type(blob) == BlobProperties and not blob.deleted:
                blobs.append({'name': blob.name,
                              'last_modified': blob.last_modified,
                              'size': self._convert_bytes(blob.size)})

        if target_path and not blobs:
            msg = 'ls: {}: No such blob'.format(original_target)
            raise Exception(msg)

        return blobs

    def _convert_bytes(self, num):
        step_unit = 1024
        for x in ['B', 'K', 'M', 'G', 'T']:
            if num < step_unit:
                return '{:3.0f}{:s}'.format(num, x)
            num /= step_unit

    def delete_blob(self, target):
        original_target = target

        if target.startswith('blob://'):
            target = target.replace('blob://', '')
        else:
            msg = 'rm: Invalid argument type'
            raise Exception(msg)

        container_name = target.split('/')[0]
        target_path = '/'.join(target.split('/')[1:])

        if container_name not in [c.name for c in self.list_contaners()]:
            msg = 'rm: {}: No such container'.format(original_target)
            raise Exception(msg)

        blob_client = self._blob_service_client.get_blob_client(
            container_name, target_path)

        if not blob_client.exists():
            msg = 'rm: {}: No such blob'.format(original_target)
            raise Exception(msg)

        blob_client.delete_blob()

        return 'delete: {}'.format(original_target)

    def transfer_blob(self, src, dst, delete_flag=False):
        original_src, original_dst = src, dst
        if src.startswith('blob://') and dst.startswith('blob://'):
            pass

        elif src.startswith('blob://'):
            pass

        elif dst.startswith('blob://'):
            dst = dst.replace('blob://', '')

            dst_split = dst.split('/', 1)
            if len(dst_split) > 1:
                container_name, dst_path = dst_split
                if os.path.basename(dst_path):
                    blob_name = dst_path
                else:
                    blob_name = os.path.join(os.path.dirname(
                        dst_path), os.path.basename(src))
            else:
                container_name = dst
                blob_name = os.path.basename(src)

            self._upload_blob(container_name, blob_name, src)

        if delete_flag:
            action_name = 'move'
        else:
            action_name = 'copy'

        return '{}: {} to {}'.format(action_name, original_src, original_dst)

    def _upload_blob(self, container_name, blob_name, src):
        blob_client = self._blob_service_client.get_blob_client(
            container_name, blob=blob_name)

        if blob_client.exists():
            blob_client.delete_blob()

        with open(src, 'rb') as f:
            blob_client.upload_blob(f)

    def _download_blob(self, container_name, blob_name):
        blob_client = self._blob_service_client.get_blob_client(
            container_name, blob=blob_name)

        with open(blob_name) as f:
            download_file.write(blob_client.download_blob().readall())
