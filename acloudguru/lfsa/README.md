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

## Labs - packaing

```bash
yum clean all
yum makecache

# Next, let's list the available updates:
yum list updates

# Finally, we need to update the software packages on the system:
yum -y update
```

```bash
yum search 'apache http'

yum provides httpd

yum -y install httpd

systemctl status httpd

systemctl enable httpd --now

systemctl status httpd.service
```

```bash
# Let's first make sure that the elinks package isn't installed:
rpm -qd httpd

# Show configuration files:
rpm -qc httpd

# Show which package owns a file (in this case /sbin/httpd):
rpm -qf /sbin/httpd

# Show all packages installed on the system:
rpm -qa | wc

# We piped this command into wc, just so our screen wouldn't be inundated with information, but we can see that there are several hundred packages installed on the system. To look at them in order of install time, from oldest to newest:
rpm -qa --last | tac

# At least this way, what's down near our new command prompt is the most recently installed packages.
# Now if we just want to see packages that start with httpd, we'd run:
rpm -qa 'httpd*'
```

## User and Group Management

```bash
useradd
adduser

usermod

userdel
deluser
```

```
cat /etc/passwd
```

And to make test1 change their password on the next login, run:
```
chage -d0 test1
```
password:
```
cat /etc/shadow
```

## Create, Delete, and Modify Local Groups and Group Memberships

```
cat /etc/group
```
GROUPNAME:x:gid:<list-of-users>

```
groupadd
addgroup
gpasswd

usermod -aG groupname useraccount
gpasswd -d username groupname
```
updates after re-login

- check own groups `groups`
- check user's groups `groups username`

switch to groups session:
```
newgrp groupname
```

edit groups file
```
sudo vigr
```

edit  sudoers:
```
visudo
```

## Manage System-Wide Environment Profiles

```
env
printenv
echo $VAR
```

Local:
- export VAR='value'

User:
- echo "export VAR='value'" >> ~/.bashrc, ~/.bash_profile, ...

System:
- export VAR='value' >> /etc/profile.d/custom.sh
- export VAR='value' >> /etc/bash.bashrc
- export VAR='value' >> /etc/environment

```
unset VAR
```

## Manage Template User Environment
```
ls -la /etc/skel
```

## Configure User Resource Limits

/etc/security/limits.conf

```txt
#<domain>      <type>  <item>         <value>
#

#*               soft    core            0
#root            hard    core            100000
#*               hard    rss             10000
#@student        hard    nproc           20
#@faculty        soft    nproc           20
#@faculty        hard    nproc           50
#ftp             hard    nproc           0
#ftp             -       chroot          /ftp
#@student        -       maxlogins       4
```

man limits.conf

```
ulimit -a
```

## Manage User Privileges

/etc/security/access.conf

permission:users:origins

```
# User "root" should be allowed to get access from hosts with ip addresses.
#+:root:192.168.200.1 192.168.200.4 192.168.200.9
#+:root:127.0.0.1

# User "john" should get access from ipv4 as ipv6 net/mask
#+:john:::ffff:127.0.0.0/127
```

## Configure PAM

- App must be PAM-aware
- /etc/pam.d
- /etc/pam.conf

```bash
$ ls /lib/x86_64-linux-gnu/security/
pam_access.so  pam_extrausers.so  pam_gnome_keyring.so  pam_localuser.so  pam_permit.so     pam_shells.so      pam_timestamp.so  pam_xauth.so
pam_cap.so     pam_faildelay.so   pam_group.so          pam_loginuid.so   pam_pwhistory.so  pam_stress.so      pam_tty_audit.so
pam_debug.so   pam_faillock.so    pam_issue.so          pam_mail.so       pam_rhosts.so     pam_succeed_if.so  pam_umask.so
pam_deny.so    pam_filter.so      pam_keyinit.so        pam_mkhomedir.so  pam_rootok.so     pam_systemd.so     pam_unix.so
pam_echo.so    pam_fprintd.so     pam_lastlog.so        pam_motd.so       pam_securetty.so  pam_tally2.so      pam_userdb.so
pam_env.so     pam_ftp.so         pam_limits.so         pam_namespace.so  pam_selinux.so    pam_tally.so       pam_warn.so
pam_exec.so    pam_gdm.so         pam_listfile.so       pam_nologin.so    pam_sepermit.so   pam_time.so        pam_wheel.so
```

PAM Workflow
- A user launches a PAM-aware application
- The app calls **libpam**
- The library checks for files in /etc/pam.d directory to see which PAM modules to load, including **system-auth**
- Each module is executed by following the rules defined for that application
![pam.png](imgs%2Fpam.png)

# Networking
## Configure Networking and Hostname Resolution Statically or Dynamically

interfaces:
```
ifconfig
```

```
$ ls -la /etc/network
total 32
drwxr-xr-x   6 root root  4096 авг 19  2021 .
drwxr-xr-x 159 root root 12288 окт 24 10:08 ..
drwxr-xr-x   2 root root  4096 авг 22 06:53 if-down.d
drwxr-xr-x   2 root root  4096 июн  2 06:49 if-post-down.d
drwxr-xr-x   2 root root  4096 апр 21  2022 if-pre-up.d
drwxr-xr-x   2 root root  4096 авг 22 06:53 if-up.d
```

Ubuntu:
```
ls /etc/netplan

ip addr show
```

Centos:
```
cd /etc/sysconfig/network-scripts
cat ifcfg-ens5

sudo ip link set ens5 down && sudo ip link set ens5 up
```

## Configure Network Services to Start Automatically at Boot

- ssh (encrypted)
- ntp
- telnet (not encrypted)

telnet:
```
systemctl status inetd
systemctl status xinetd
sudo apt-get install telnetd telnet
```

`cat /etc/services`

## Implement Packet Filtering

- iptables -L

DROP configuration for ICMP:
```
iptables -A INPUT -p icmp -i ens5 -j DROP
-A - append
-p - protocol
-i - name of interface
-j - target rule
```

```
iptables --flush
```

## Start, Stop, and Check the Status of Network Services

```
netstat -ie
```

```
$ netstat -r
Kernel IP routing table
Destination     Gateway         Genmask         Flags   MSS Window  irtt Iface
default         _gateway        0.0.0.0         UG        0 0          0 wlp2s0
link-local      0.0.0.0         255.255.0.0     U         0 0          0 wlp2s0
172.17.0.0      0.0.0.0         255.255.0.0     U         0 0          0 docker0
172.18.0.0      0.0.0.0         255.255.0.0     U         0 0          0 br-e210288b8efa
172.19.0.0      0.0.0.0         255.255.0.0     U         0 0          0 br-2dbe025c4f2c
192.168.0.0     0.0.0.0         255.255.255.0   U         0 0          0 wlp2s0
192.168.49.0    0.0.0.0         255.255.255.0   U         0 0          0 br-e01d5ac90408
```

all sockets for tcp:
```
netstat -at
```
udp:
```
netstat -au
```
statistics:
```
netstat -su
netstat -st
```

## Statically Route IP Traffic
```
ip addr show
```

```
route -n
ip route show
```

```
traceroute 8.8.8.8
```

forwarding:
```
$ sysctl net.ipv4.ip_forward
net.ipv4.ip_forward = 1
```

```
ip route add 8.8.0.0/16 proto static metric 10 via inet 192.168.1.1 12 dev enp0s5
```

```
ip route del 8.8.0.0/16 proto static metric 10 via inet 192.168.1.1 12 dev enp0s5
```

## Synchronize Time Using Other Network Peers

```
timedatectl
```

enable/disable sync:
```
timedatectl set-ntp on/off
```

view and update TZ:
```
timedatectl list-timezones
timedatectl set-timezone TIMEZONE
```

## Adding an IP Address and a Static Route

```
ip a add 10.0.5.20/24 dev ens5
ip a del 10.0.5.20/24 dev ens5
```

```
ip r add 10.0.6.0/24 via 10.0.5.5 dev ens5
ip r del 10.0.6.0/24 via 10.0.5.5 dev ens5
```

# Service Configuration
## Configure a Caching DNS Server

- /etc/bind/named.conf.options
- apt install bind9 bind9utils bind9doc

## Maintain a DNS Zone

Component of a DNS Zone:
- Zone entry - named.conf.local
- Forward lookup zone file
- Reverse lookup zone file

Content of a Zone file
- SOA
- NS
- A
- NX
- CN

```
sudo named-checkconf
sudo systemctl restart bind9
```

## Configure Email Aliases

```
cd /etc/postfix; ls -la;
nano aliases
postalias /etc/postfix/aliases
```

## Configure SSH Servers and Clients
/etc/ssh/sshd_config

/etc/ssh/ssh_config

~/.ssh/config

```
ssh-keygen
```

```
ssh-copy-id cloud_user@<remote-host>
```
## Restrict Access to HTTP Proxy Servers

/etc/squid/squid.conf

## Configure an IMAP and IMAPS Service (and Pop3 and Pop3S)

cat /etc/dovecot/dovecot.conf

## Query and Modify the Behavior of System Services at Various Operating Modes

```
systemctl cat apache2

systemctl edit cups

rm -rf /etc/systemd/system/cups.service.d/

systemctl daemon-reload

systemctl edit --full cups

systemctl list-dependancies cups

systemctl list-units --type=service
systemctl list-units --type=service --state=inactive
systemctl list-units --type=service --state=active
```

## Configure an HTTP Server (Ubuntu/Debian)

```
/var/www/html

ls -lah /etc/apache2

/etc/apache2/site-available/000-default.conf

/etc/apache2/site-enabled/

apachectl configtest

/var/log/apache2
```

## Configure HTTP Server Log Files

```
cat /etc/apache2/apache2.conf | grep LogFormat
```

## Restrict Access to a Web Page

Make backup of the conf file before making changes
```
<Directory /var/www/html/test/>
   Order allow,deny
   Allow from 192.168.1.50
   Allow from 192.168.26   
   Allow from 127
</Directory>
```

## Configure a Database Server

- disable anonymous accounts when possible
- disable remote root logon access when possible

## Manage and Configure Containers
```
docker ps
docker image list
docker run
docker start/stop
docker rm
```

## Manage and Configure Virtual Machines
vm extensions:
```
cat /proc/cpuinfo | grep vmx
```
- if no - use `qemu`

```
virt-install
virt-clone
virt-managed
virsh 
```

```
virsh-install --name=tiny --vcpus=1 --memory=1024 --cdrom=alpine-standard-3.10.3-x86.iso --disk size=5
```

```
virsh list --all
```

# Storage Management

## List, Create, Delete, and Modify Physical Storage Partitions

```
lsblk - list block devices
fdisk, parted - manage disk partitions
```

```
sudo fdisk /dev/sdb

m - help

w
```

```
parted /dev/sdb

resizepart
2
1024
```

## Manage and Configure LVM Storage Part 1 - Create LVM

LVM - allows you to join multiple physical disks together in such a way that they are presented to the OS as a single disk

- pvcreate /dev/disk1 /dev/disk2
- pvdisplay
- vgcreate vgname /dev/disk1 /dev/disk2
- vgdisplay
- lvcreate --name lvname --size xxxM vgname
- lvdispaly

```
mkfs.ext4 /dev/vg01/lv01
mkdir -p /mnt/data
mount /dev/vg01/lv01 /mnt/data
```

## Manage and Configure LVM Storage Part 2 - Extend LVM

```
pvs

vgs

vgextend vgname /dev/disk1

lvs

lvextend -l EXTENTS /dev/vgname/lvname
```

```
pvcreate /dev/sdc3
pvs
pvdisplay
```

```
vgs
vgdisplay
```

```
vgextend vg01 /dev/sdc3
vgs
pvs
lvs
resize2fs /dev/vg01/lv01
df -h
```

```
pvmove
pvremove
...
```

## Create and Configure Encrypted Storage

check if module is loaded:
```
grep -i config_dm_crypt /boot/config-$(uname -r)
```

To create an encrypted partition:
```cryptsetup -y luksFormat /path/partition```

To open an encrypted partition:
```cryptsetup luksOpen /path/partition fsname```

To close an encrypted partition:
```
umount /mnt/filesystem
cryptsetup luksClose fsname
```

## Configure Systems to Mount File Systems at or During Boot

- /etc/fstab

## Configure and Manage Swap Space

- A file, partition, or combination of the two used to store inactive pages of memory to free up RAM for system use
- Not an alternative to RAM, just a temporary fix as swap is much slower because the pages are written to a disk and no longer redident in memory

```
swapon --show

$ free
              total        used        free      shared  buff/cache   available
Mem:       32423648    12857740     6452608     1286004    13113300    17826232
Swap:       2097148     1057432     1039716

htop
```

```
sudo swapoff -a

sudo swapon -a
```

```
fallocate ...
dd ...
mkswap /swapfile2
```

## Create and Manage RAID Devices

```
lsblk
fdisk /dev/sdc
```

```
mdadm --create --verbose /dev/md0 --level=0 --raid-devices=2 /dev/sdc1 /dev/sdc2

cat /proc/mdstat

mdadm --detail /dev/dm0

mkfs.ext4 /dev/md0
mount /dev/md0 /mnt/raid
```

```
mdadm --detail --scan
nano /etc/mdadm/mdadm.conf

mdadm --assemble --scan
update-initramfs -u
```

`nano /etc/fstab`
```
/dev/md0 /mnt/raid ext4 default 0 0
```

## Configure Systems to Mount File Systems on Demand
```
yum install samba-client samba-common cifs-utils
```

```
smbclient -L REMOTESYSTEM
```

## Create, Manage, and Diagnose Advanced File System Permissions

- sticky bit - permission set on a directory that allows only the owner or the root user to delete or rename contents within the dir
- setgid
- setuid - permission set on a file so that when an executable is launched, it will run with owner's privileges rather than the user

set sticky bit:
```
chmod 1770 directory
```

## Set up User and Group Disk Quotas for File Systems

- /etc/fstab
  - add usrquota and/or grpquota options to the entry
- run the `quotacheck` cmd to create user and/or group quota files
- use `quotaon` command to turn on quotas for a filesystem

```
edquota -u username

quota -vs username

repquota -asgu
```
