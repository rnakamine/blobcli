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
        list_containers = [
            c for c in self._blob_service_client.list_containers() if not c.deleted]
        return list_containers

    def _extract_container_name(self, path):
        container_name = path.split('/')[0]
        path = '/'.join(path.split('/')[1:])
        if not path:
            path = None
        return container_name, path

    def _convert_bytes(self, num):
        step_unit = 1024
        for x in ['B', 'K', 'M', 'G', 'T']:
            if num < step_unit:
                return '{:3.0f}{:s}'.format(num, x)
            num /= step_unit

    def list_blobs(self, target):
        original_target = target

        if target.startswith('blob://'):
            target = target.replace('blob://', '')
        container_name, target_path = self._extract_container_name(target)

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

    def delete_blob(self, target):
        original_target = target

        if target.startswith('blob://'):
            target = target.replace('blob://', '')
        else:
            msg = 'rm: Invalid argument type'
            raise Exception(msg)

        container_name, target_path = self._extract_container_name(target)
        blob_client = self._blob_service_client.get_blob_client(
            container_name, target_path)

        if not blob_client.exists():
            msg = 'rm: {}: No such container or blob'.format(original_target)
            raise Exception(msg)

        blob_client.delete_blob()

        return 'delete: {}'.format(original_target)

    def _upload_blob(self, container_name, blob_name, src):
        blob_client = self._blob_service_client.get_blob_client(
            container_name, blob=blob_name)

        with open(src, 'rb') as f:
            blob_client.upload_blob(f, overwrite=True)

    def _upload_blob_from_blob_storage(self, src_container_name, src_blob_name, dst_container_name, dst_blob_name):
        src_blob_client = self._blob_service_client.get_blob_client(
            src_container_name, src_blob_name)
        dst_blob_client = self._blob_service_client.get_blob_client(
            dst_container_name, dst_blob_name)

        if not src_blob_client.exists():
            msg = 'rm: blob://{}/{}: No such container or blob'.format(
                src_container_name, src_blob_name)
            raise Exception(msg)

        stream = src_blob_client.download_blob().readall()
        dst_blob_client.upload_blob(stream, overwrite=True)

    def _download_blob(self, container_name, blob_name, dst):
        blob_client = self._blob_service_client.get_blob_client(
            container_name, blob=blob_name)

        if not blob_client.exists():
            msg = 'rm: blob://{}/{}: No such container or blob'.format(
                container_name, blob_name)
            raise Exception(msg)

        with open(dst, 'wb') as f:
            f.write(blob_client.download_blob().readall())

    def transfer_blob(self, src, dst, delete_flag=False):
        original_src, original_dst = src, dst

        # blob storage to blob storage
        if src.startswith('blob://') and dst.startswith('blob://'):
            src = src.replace('blob://', '')
            dst = dst.replace('blob://', '')
            src_container_name, src_blob_name = self._extract_container_name(
                src)
            dst_container_name, dst_blob_path = self._extract_container_name(
                dst)

            if dst_blob_path:
                if dst_blob_path.endswith('/'):
                    dst_blob_name = os.path.join(
                        dst_blob_path, os.path.basename(src_blob_name))
                else:
                    dst_blob_name = dst_blob_path
            else:
                dst_blob_name = os.path.basename(src_blob_name)

            self._upload_blob_from_blob_storage(
                src_container_name, src_blob_name, dst_container_name, dst_blob_name)
            if delete_flag:
                self.delete_blob(
                    'blob://{}/{}'.format(src_container_name, src_blob_name))

        # blob storage to local
        elif src.startswith('blob://'):
            src = src.replace('blob://', '')
            container_name, blob_name = self._extract_container_name(src)

            if dst.endswith('/') or dst == '.':
                dst = os.path.join(dst, os.path.basename(blob_name))

            self._download_blob(container_name, blob_name, dst)
            if delete_flag:
                self.delete_blob(
                    'blob://{}/{}'.format(container_name, blob_name))

        # local to blob storage
        elif dst.startswith('blob://'):
            dst = dst.replace('blob://', '')
            container_name, dst_path = self._extract_container_name(dst)

            if dst_path:
                if dst.endswith('/'):
                    blob_name = os.path.join(os.path.dirname(
                        dst_path), os.path.basename(src))
                else:
                    blob_name = dst_path
            else:
                blob_name = os.path.basename(src)

            self._upload_blob(container_name, blob_name, src)
            if delete_flag:
                os.remove(src)

        if delete_flag:
            action_name = 'move'
        else:
            action_name = 'copy'
        return '{}: {} to {}'.format(action_name, original_src, original_dst)
