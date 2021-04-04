# blobcli

[![PyPI version](https://badge.fury.io/py/blobcli.svg)](https://badge.fury.io/py/blobcli)
[![MIT License](http://img.shields.io/badge/license-MIT-blue.svg?style=flat)](LICENSE)

This is a command line interface for easy operation with blobs in Azure Blob Storage.

## Installation

```sh
$ pip install blobcli
```

## Usage
Set connection string to environment variable
```sh
$ export AZURE_STORAGE_CONNECTION_STRING="<yourconnectionstring>"
```

```sh
$ blobcli
Usage: blobcli [OPTIONS] COMMAND [ARGS]...

  blob storage easy operation cli (v0.0.2)

Options:
  --help  Show this message and exit.

Commands:
  cp  Copy blob.
  ls  List containers or blobs.
  mv  Move blob.
  rm  Delete blob.
```

### List containers or blobs
```sh
$ blobcli ls <target>
```

Show list of containers
```sh
$ blobcli ls
2021-04-04 12:41:09+00:00 samplecontainer01
2021-04-04 12:41:19+00:00 samplecontainer02
2021-04-04 12:41:26+00:00 samplecontainer03
```

Show list of blobs for the specified container
```sh
$ blobcli ls samplecontainer01
                            PRE sample-dir01/
                            PRE sample-dir02/
2021-04-04 12:43:49+00:00    0B sample01.txt
2021-04-04 12:43:54+00:00    0B sample02.txt
2021-04-04 12:43:58+00:00    0B sample03.txt
```

```sh
$ blobcli ls samplecontainer01/sample-dir01/
2021-04-04 12:56:27+00:00    0B sample04.txt
2021-04-04 12:57:27+00:00    0B sample05.txt
```

### Delete blob
```sh
$ blobcli rm <target>
```

Delete the specified blob
```sh
$ blobcli rm blob://samplecontainer01/sample03.txt
delete: blob://samplecontainer01/sample03.txt
```

### Move blob
```sh
$ blobcli mv <source> <target> 
```

Move blob from local to container
```sh
$ blobcli mv sample05.txt blob://samplecontainer01/sample-dir01/
move: sample05.txt to blob://samplecontainer01/sample-dir01/
```

container to local
```sh
$ blobcli mv blob://samplecontainer01/sample-dir01/sample05.txt .
move: blob://samplecontainer01/sample-dir01/sample05.txt to .
```

container to container
```sh
$ blobcli mv blob://samplecontainer01/sample01.txt blob://samplecontainer02/sample11.txt
move: blob://samplecontainer01/sample01.txt to blob://samplecontainer02/sample11.txt
```

### Copy blob
```sh
$ blobcli cp <source> <target>
```

Copy blob from local to container
```sh
$ blobcli cp sample05.txt blob://samplecontainer01/sample-dir01/
copy: sample05.txt to blob://samplecontainer01/sample-dir01/
```

container to local
```sh
$ blobcli cp blob://samplecontainer01/sample-dir01/sample05.txt .
copy: blob://samplecontainer01/sample-dir01/sample05.txt to .
```

container to container
```sh
$ blobcli cp blob://samplecontainer01/sample01.txt blob://samplecontainer02/sample11.txt
copy: blob://samplecontainer01/sample01.txt to blob://samplecontainer02/sample11.txt
```

## License
This project are released under the [MIT License](LICENSE)
