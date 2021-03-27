from setuptools import setup

setup(
    install_requires=['Click', 'azure-storage-blob'],
    entry_points='''
        [console_scripts]
        blobcli=blobcli.cli:cli
    '''
)
