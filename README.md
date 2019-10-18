[![PyPI version](https://badge.fury.io/py/partialCopy.svg)](https://badge.fury.io/py/partialCopy)

# partialCopy
A tool to copy big data to multiple smaller disks

## Motivation

As the storage becomes larger in big projects, we need to a tool to break large folders (100 TBs) to smaller chunks, so we can migrate to another location or storing it on tapes.

## How does it work?

The tool finds the best placement for the files and it creates a files list in --save-to directory which can be passed rsync using `--files-from` parameter.
## Installation

```sudo pip install partialCopy```

## Usage
```
usage: pcp.py [-h] [--dest DEST | --dest-size DEST_SIZE] [-s SAVE_TO] [-f]
              [-n] [-ma MODIFIED_AFTER] [-fp FIND_PARAMS]
              src

positional arguments:
  src                   Source Directory

optional arguments:
  -h, --help            show this help message and exit
  --dest DEST           Destionation mountpoint
  --dest-size DEST_SIZE
                        Destination size, given in bytes or using 1 letter
                        unit B,K,M,G,T,P
  -s SAVE_TO, --save-to SAVE_TO
                        Where to save rsync list,default
                        '$src/pcp_rsync_list/'
  -f, --force           Rewrite all lists again
  -n, --new             Find New Files
  -ma MODIFIED_AFTER, --modified-after MODIFIED_AFTER
                        Find files modified after certain time (YYYY-mm-dd)
  -fp FIND_PARAMS, --find-params FIND_PARAMS
                        Parameters to find command

```
## Changes
* Allowing to provide size rather than mount point.
* Finds only new files using `-n` parameter.
* Finds files modified after a certain date using `-ma` parameter.
* Allows rewriting all lists using `-f` flag.  


# Contributors
* [Zeeshan Ali Shah](https://github.com/zeeshanali)
