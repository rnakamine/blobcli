# blobcli

[![MIT License](http://img.shields.io/badge/license-MIT-blue.svg?style=flat)](LICENSE)

This is a command line interface to handle Blobs in Azure Blob Storage like a UNIX command.

## Installation

```sh
$ pip install blobcli
```

## Usage
Set connection string to environment variable
```sh
$ export AZURE_STORAGE_CONNECTION_STRING="<yourconnectionstring>"
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

### Copy blob
```sh
$ blobcli cp <source> <target>
```
