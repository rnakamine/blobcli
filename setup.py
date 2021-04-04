import os

from setuptools import setup, find_packages


description = 'This is a command line interface for easy operation with blobs in Azure Blob Storage.'
long_description = description
if os.path.exists('README.md'):
    long_description = open('README.md').read()

setup(
    name="blobcli",
    version='0.0.1',
    packages=find_packages(),
    author='Ryo Nakamine',
    author_email='rnakamine8080@gmail.com',
    url='https://github.com/rnakamine/blobcli',
    description=description,
    long_description=long_description,
    long_description_content_type='text/markdown',
    python_requires='~=3.6',
    install_requires=['Click', 'azure-storage-blob'],
    entry_points='''
        [console_scripts]
        blobcli=blobcli.cli:main
    ''',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Operating System :: OS Independent',
    ],
)
