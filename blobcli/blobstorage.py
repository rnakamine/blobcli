import os

from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
blob_service_client = BlobServiceClient.from_connection_string(connect_str)


def list_contaners():
    containers = blob_service_client.list_containers()
    return containers


def list_blobs(target):
    if not target.startswith('blob://'):
        pass

    if target.endswith('/'):
        target = target[:-1]

    target = target.replace('blob://', '').split('/')
    container_name = target[0]
    blob_path = '/'.join(target[1:])

    container_client = blob_service_client.get_container_client(
        container_name)

    blobs = []
    for blob in container_client.list_blobs():
        if blob_path:
            if blob_path in blob.name:
                blob_name = blob.name.replace(
                    blob_path + '/', '').split('/')
            else:
                continue
        else:
            blob_name = blob.name.split('/')

        # check directory or file
        if len(blob_name) > 1:
            blobs.append({'name': blob_name[0] + '/',
                          'last_modified': None})
        else:
            blobs.append({'name': blob_name[0],
                          'last_modified': blob.last_modified})

    return blobs
