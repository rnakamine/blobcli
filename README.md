# [WIP] blobcli

[![MIT License](http://img.shields.io/badge/license-MIT-blue.svg?style=flat)](LICENSE)

This is a command line interface to handle Blobs in Azure Blob Storage like a UNIX command.

## Installation

```sh
$ pip install blobcli
```

## Usage

### List blobs
```sh
$ blobcli ls <target>
```

### Delete blob
```sh
$ blobcli rm <target>
```

### Move blob
```sh
$ blobcli mv <source> <target> 
```

### Copy blob
```sh
$ blobcli cp <source> <target>
```
