# partialCopy
A tool to copy big data to multiple smaller disks

## Motivation

As the storage becomes larger in big projects, we need to a tool to break large folders (100 TBs) to smaller chunks to be allow to migrate to another location or storing it on tapes.

## How does it work?

The tool finds the best placement for the files and it creates a files list in --save-to directory which can be to rsync using `--files-from`
parameter.
## Installation

```sudo pip install partialCopy```

## Usage
```
usage: pcp [-h] [-s SAVE_TO] [-fp FIND_PARAMS] src dest

positional arguments:
  src                   Source Directory
  dest                  Dest Mountpoint

optional arguments:
  -h, --help            show this help message and exit
  -s SAVE_TO, --save-to SAVE_TO
                        Where to save rsync list
  -fp FIND_PARAMS, --find-params FIND_PARAMS
                        Parameters to find command
```

# Contributors
* [Zeeshan Ali Shah](https://github.com/zeeshanali)
