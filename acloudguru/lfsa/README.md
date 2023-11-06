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

## Use Input-Output Redirection (e.g. >, >>, |, 2>)
FDs:
- stdin, stdout, stderr

Redirection:
- pipe (|)
- create / overwrite (>)
- >>
- <

## Analyze Text Using Basic Regular Expressions
```
grep '^The ' filename
grep '^T[a-z]^[e]' filename.txt
...
```

## Archive, Backup, Compress, Unpack, and Decompress Files
```
tar
```

## Create, Delete, Copy, and Move Files and Directories
```
touch, nano, cp, mv, mkdir, rm, rmdir (only if dir is empty), rm -r
```

## Create and Manage Hard and Soft Links

Hard link
- direct pointer to file (inode)
- can only be a file
- shares the same inode as source
- as long as hard link exists, the data exists

```
ln info.txt infohardlink
ls -lhF

ls -li # the same inode
```

Soft link (Symbolink link)
- A redirect to file (think shorcut or alias)
- Can be a file or directory
- Has a unique inode (own)
- Can be on a different filesystem or mounted share
- If the source file is deleted, the soft link is broken

```
ln -s details.txt detailssoftlink
ls -lhF
```

## List, Set, and Change Standard File Permissions

special permission:
```
suid = s     4000
sguid = s    2000
sticky = t   1000
```

```
chmod 777 filename 
chmod u+rwx filename; chmod g+rwx filename; chmod o+rwx filename
```

```
chmod 755 filename
chmod g-x filename; chmod u-x filename; chmod o-x filename
```

```
chown
```

Several file systems support **file attributes** that enable further customization of allowable file operations. File attributes (make immutable):
```
sudo chattr +i start.sh
lsattr start.sh
```
Read more: https://wiki.archlinux.org/title/File_permissions_and_attributes#File_attributes

## Manage Access to the root Account

Evelator command:
```
sudo command
```

```
su - substitute user
```
- access is granted via entries in the `/etc/sudoers` file
- access can be managed by account or by group

## Read and Use System Documentation

- man pages
- info pages
- help pages
- `whatis` command

# Boot, Reboot, and Shut Down a System Safely

- shutdown -r <TIME>, reboot
- shutdown -H <TIME>, halt
- shutdown -P <TIME>, poweroff
```
$ ls -la /sbin/shutdown 
lrwxrwxrwx 1 root root 14 Mar  2  2023 /sbin/shutdown -> /bin/systemctl
```

## Boot or Change System into Different Operating Modes

Init is the first process started when a computer boots up
and is the direct or indirect parent of all other processes.

Runlevels:
- 0 - system halt
- 1 - single user mode
- 2 - Multi-user
- 3 - Multi-user with network
- 4 - Experemental
- 5 - Multi-user with network and graphical mode (as your desktop)
- 6 - Reboot

```
$ runlevel
N 5

$ systemctl get-default
graphical.target
```

## Install, Configure, and Troubleshoot Boot-Loaders

GRUB2 - boot-loader

```
$ cat /boot/grub/grub.cfg

$ ls -l /etc/grub.d/
total 136
-rwxr-xr-x 1 root root 10627 авг 12  2021 00_header
-rwxr-xr-x 1 root root  6258 авг 12  2021 05_debian_theme
-rwxr-xr-x 1 root root 18224 янв 11  2022 10_linux
-rwxr-xr-x 1 root root 42359 авг 12  2021 10_linux_zfs
-rwxr-xr-x 1 root root 12894 авг 12  2021 20_linux_xen
-rwxr-xr-x 1 root root  1992 авг 18  2020 20_memtest86+
-rwxr-xr-x 1 root root 12059 авг 12  2021 30_os-prober
-rwxr-xr-x 1 root root  1424 авг 12  2021 30_uefi-firmware
-rwxr-xr-x 1 root root   700 фев 21  2022 35_fwupd
-rwxr-xr-x 1 root root   214 авг 12  2021 40_custom
-rwxr-xr-x 1 root root   216 авг 12  2021 41_custom
-rw-r--r-- 1 root root   483 авг 12  2021 README

$ cat /etc/default/grub

$ update-grub
```

## Diagnose and Manage Processes
- top
- htop
- ps, `ps -ef`, `ps aux`

- `sudo nice -n -10 /bin/bash`
- `sudo renice -n 20 12705`

## Locate and Analyze System Log Files

Ubuntu/Debian:
```
ls /var/log
```

```
less /var/log/syslog
cat /var/log/syslog | grep apparmor
```

CentOS:
```
cat /var/log/boot.log
cat /var/log/messages
```

## Schedule Tasks to Run at a Set Date and Time

`crontab -e`

## Verify Completion of Scheduled Jobs

## Update and Manage Software to Provide Required Functionality and Security, Part 1 - Ubuntu/Debian

```bash
# install
dpkg -i filename.deb

# list
dpkg -l

# remove package
dpkg -r pkgname 
```

```bash
sudo aptitude
```

```
apt

apt-get
```

## Update and Manage Software to Provide Required Functionality and Security, Part 2 - CentOS/Redhat

```
rpm -ivh filename.rpm (install)
rpm -Uvh filename.rpm (upgrade)
rpm -qa (list installled pkgs)
rpm -e filename.rpm (upgrade)
```

```
yum install/remove/update/list/search
dnf install/remove/update/list/search
```

## Verify the Integrity and Availability of Resources

Unmount and check fs (never check a mounted fs):
```
sudo umount /path/to/fs
sudo fsck /path/to/fs
```

## Verify the Integrity and Availability of Key Processes

```
ps
top/htop
```

## Change Kernel Runtime Parameters, Persistent and Non-Persistent

non-persistence
```bash
sysctl -a
sysctl dev.cdrom.autoclose
sysctl -w dev.cdrom.autoclose=0
sysctl -p  (load the new configuration, by default /etc/sysctl.conf)
```
```
ls -al /proc/sys
echo 0 > /proc/sys/dev/cdrom/autoclose
```

persistent:
```
nano /etc/sysctl.d/99_my_sysctls.conf
sysctl -p /etc/sysctl.d/99_my_sysctls.conf

service procps start
```

## Use Scripting to Automate System Maintenance Tasks

shebang:
```
#!/bin/bash
#!/bin/zshell
#!/bin/dash
```

## Scripting Conditionals and Loops Part 1 - Operators/If

```
read -p "Enter a number for a: ' a
read -p "Enter a number for b: ' b
```

```
-eq
-gt
-lt
```

```
if [ a = b ]; then
  echo True
else
  echo False
fi
```

filecheck:
```
if [ -f $FILE ]; then
  echo "$FILE exists"
fi
```

## Scripting Conditionals and Loops Part 2 - For/While/Until

```
for x in 1 2 3
do
  echo "x = " $x
done
```

```
while read url
do
  curl "$url" >> output.html
done < listofurls.txt
```

## Manage the Startup Process and Services (In Services Configuration)

```
systemctl status <service>

systemctl start <service>
systemctl stop <service>
systemctl restart <service>

systemctl enable <service>
systemctl disable <service>
```

## List and Identify SELinux/AppArmor File and Process Contexts

SELinux - Centos
```bash
sudo semanage fcontext -l 
sudo semanage fcontext -l | grep sshd
```
context info for every file, dir and process on the system.

- Enforce mode - access is not allowed
  ```bash
  getenforce (will return the SELinux mode)
  setenforce (will update the SELinux mode)
  ```
- Passive mode - log the infraction
- Disabled - nothing happens
```
ls -Z
ps auxZ  |grep cron
```


AppArmor - Ubuntu
- /etc/apparmor.d/

```
sudo aa-status
cat /etc/apparmor.d/usr.sbin.tcpdump
```

```
ps auxZ
```

```
aa-enabled (returns whether AppArmor is enabled)

aa-disable (will disable an AppArmor security profile)
aa-enable (set enable)
aa-complain (set complain)
```