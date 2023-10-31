# Essential Commands

## Search for Files Part 1 - Find/Locate

`find` vs `locate`:
- locate relies on db for search, faster than find

```bash
find /etc -name "search.txt"
find /etc -iname "search.txt"

find / -type f -name "*.log"
find /etc -type f -user kirill

man find 
```

```bash
sudo updatedb
locate "search.txt"
locate -i "search.txt"
```

## Search for Files Part 2 - Which/Whereis/Type

- which - returns the location of a command based on the PATH settings
- whereis - return multiple versions of a file if they exists
- type - indicate how it would be interpreted if used as a command name

```bash
whereis python | tr " " '\n'
python:
/usr/bin/python3.8-config
/usr/bin/python3.8
/usr/bin/python2.7
/usr/lib/python3.9
/usr/lib/python3.8
/usr/lib/python2.7
/etc/python3.8
/etc/python2.7
/usr/local/lib/python3.8
/usr/local/lib/python2.7
/usr/include/python3.8
/usr/share/python
/opt/az/bin/python3.10
/opt/az/bin/python3.10-config
```

```bash
type ls
ls is aliased to `ls --color=auto'
```

## Evaluate and Compare the Basic File System Features and Options
- ext4

block device (hdd/sdd,CD,flash) -> filesystem (method of allowing OS to interact with data on BD)

Journaling helps to prevent data loss during power issues. Impacts to performance

FS:
- ext4 (commodity) - max file size 16TB, journal checksums and delayed allocation
- btrfs - efficent handling of small files and directory indexes
- ...
- ZFS - supports drive pooling, FS snapshots, fs striping, each file has checksum
- XFS - handles large files well but does suffer performance issues with many small files
- JFS - ...
- Swap - not technically a FS, used for virtual memory (memory swapping) and doesn't have a viewable structure
- FAT32 - microsoft, usb drives

## Compare and Manipulate File Content and Use Input-Output Redirection Part 1 - Create Files/Input-Output

- cat
- more, less, sort - less could search - "/"
- touch
- nano

## Compare and Manipulate File Content and Use Input-Output Redirection Part 2 - Compare Files (Diff/Compare/CMP
- diff - compare line by line, could compare directories
- comm - must be sorted
- cmp - byte by byte, returns the position of the first difference