# The filesystem

## Table of contents

- [1. Bad and good news](#1-bad-and-good-news)
- [2. Pathnames](#2-pathnames)
    - [2.1. Absolute and relative pathnames](#21-absolute-and-relative-pathnames)
- [3. Mounting and unmounting](#3-mounting-and-unmounting)
    - [3.1. Mounting](#31-mounting)
    - [3.2. Unmounting](#32-unmounting)
- [4. File tree layout](#4-file-tree-layout)
- [5. File types](#5-file-types)
    - [5.1. Regular files](#51-regular-files)
    - [5.2. Directories](#52-directories)
    - [5.3. Hard links](#53-hard-links)
    - [5.4. Symbolic links](#54-symbolic-links)
    - [5.5. Character and block device files](#55-character-and-block-device-files)
    - [5.6. Named pipes](#56-named-pipes)
    - [5.7. Local domain sockets](#57-local-domain-sockets)
- [6. File attributes](#6-file-attributes)
    - [6.1. Permission bits](#61-permission-bits)
    - [6.2. Set-UID and set-GID bits](#62-set-uid-and-set-gid-bits)
    - [6.3. Sticky bit](#63-sticky-bit)
    - [6.4. Listing and inspecting files](#64-listing-and-inspecting-files)
    - [6.5. Changing permissions](#65-changing-permissions)
        - [6.5.1. Octal syntax](#651-octal-syntax)
        - [6.5.2. Mnemonic syntax](#652-mnemonic-syntax)
    - [6.6. Changing ownership](#66-changing-ownership)
- [Glossary](#glossary)
- [Bibliography](#bibliography)
- [Licenses](#licenses)

## 1. Bad and good news

The filesystem can be thought of as comprising four main components

| Component       | Description                                                   |
| --------------- | ------------------------------------------------------------- |
| Namespace       | A way to name objects and organize them in a hierarchy        |
| API             | A set of system calls for navigating and manipulating objects |
| Security models | Schemes for protecting, hiding, and sharing objects           |
| Implementation  | Software to tie the logical model to the hardware             |

Modern kernels define an abstract interface that accommodates many different filesystems

---

Some portions of the filesystem are handled by traditional disk-based implementations. The kernel support various type of disk-based implementations, such as ext4, XFS, UFS, FAT, etc.

Some portions are handled by drivers within the kernel. For example, network filesystems are handled by a driver that forwards the requested operations to a server on another computer

The bad news is that the filesystem looks like a Frankenstein's monster

---

The basic purpose of a filesystem is to name and organize storage resources (i.e., data files). However, programmers have been eager to avoid reinventing the wheel when it comes to managing other types of objects

It has often proved convenient to map these objects into the filesystem namespace. For example, device files define a way for programs to communicate with drivers inside the kernel
- Device files are not really data files
- But they are handled through the filesystem

The good news is that the filesystem provides a consistent interface

## 2. Pathnames

The filesystem is a single unified hierarchy that starts at the directory `/` and continues downward through an arbitrary number of subdirectories

`/` is the root directory

A pathname is 
- The list of directories that must be traversed to locate a particular file
- The name of that file

---

```shell
$ pwd 
/home/ubuntu/cpu-logger
$ ls
app.py  requirements.txt
```

- `app.py` and `requirements.txt` are names of files
- `/home/ubuntu/cpu-logger` is the list of directories that must be traversed to find those files
- `/home/ubuntu/cpu-logger/app.py` is a pathname

### 2.1. Absolute and relative pathnames

Pathnames can be either absolute or relative
- Relative pathnames are interpreted starting at the current working directory (use `cd` to change the shell working directory)
- Absolute pathnames are interpreted starting at `/`

```shell
$ pwd 
/home/ubuntu/cpu-logger
$ ls
app.py  requirements.txt
```

- `app.py` is a relative pathname
- `/home/ubuntu/cpu-logger/app.py` is an absolute pathname

The terms filenames, pathnames, and path are more or less interchangeable

## 3. Mounting and unmounting

The filesystem is composed of smaller chunks, which are also called filesystems. Each of these consists of one directory and its subdirectories and files

Henceforth, the term file tree will refer to the overall layout. The term filesystem will be reserved to the "branches" attached to the tree

A filesystem can be anything that obeys to the proper API, from a disk partition to a network file server or a kernel component. Most kernels also provides a "loop" filesystem that let you mount individual files as if they were distinct devices 

### 3.1. Mounting

In most situations, filesystems are attached to the tree with the `mount` command. `mount` maps a directory within the existing file tree, called the mount point, to the root of the newly attached filesystem

The previous contents of the mount point become temporarily inaccessible as long as another filesystem is mounted there. However, mount points are usually empty directory

```shell
$ mount /dev/sda4 /mnt
```

mounts the filesystem stored on the disk partition `/dev/sda4` under the path `/mnt` in the file tree

---

The `/etc/fstab` file lists the filesystems that can be mounted

```shell
$ cat /etc/fstab
LABEL=cloudimg-rootfs   /                ext4        [...]  
LABEL=BOOT              /boot            ext4        [...]
LABEL=UEFI              /boot/efi        vfat        [...]
```

- `LABEL`: a human-friendly name that refers to a disk partition
- `/`, `/boot`,  and `/boot/efi`: mount points
- `ext4` and `vfat`: filesystem types

### 3.2. Unmounting

The `umount` command is to detach filesystems from the file tree. A filesystem can be unmounted if there are no
- Open files
- Processes whose current current directories are located there
- Executable files that are running

```shell
$ umount /mnt
$ umount /
umount: /: must be superuser to unmount.
$ sudo umount /
[sudo] password for ubuntu:
umount: /: target is busy.
```

---

The `umount` command also provides a lazy unmount option (`umount -l`) that removes a filesystem from the naming hierarchy but does not truly unmount it until all existing file references have been closed. However
- Bear in mind that there is no guarantee that existing references will ever close on their own
- Lazy unmounted filesystems present inconsistent semantics to the programs that are using them. For example, programs can read and write open files but cannot open new files

---

When a filesystem is busy, a good idea is to find out which processes hold references to that filesystem. The `fuser` command with the `-m` option prints who is using a mounted filesystem 

```shell
$ sudo fuser -v -m /proc
                     USER        PID ACCESS COMMAND
/proc:               root     kernel mount /proc
                     root          1 f.... systemd
                     root        281 f.... systemd-journal
                     root        641 f.... udisksd
                     syslog      675 f.... rsyslogd
                     ubuntu    32713 f.... systemd
```

- the kernel has mounted `/proc`
- `systemd` (`PID 1`) has an open file (`f`) in `/proc`

---

| Access | Meaning                              |
| ------ | ------------------------------------ |
| `c`    | Current directory                    |
| `e`    | Executable being run                 |
| `f`    | Open file                            |
| `F`    | Open file for writing                |
| `r`    | Root directory                       |
| `m`    | Memory-mapped file or shared library |
| `.`    | Placeholder                          |

---

The `fuser` command with no `-m` option checks who is using a specific file

```shell
$ cd cpu-logger
$ fuser -v /home/ubuntu/cpu-logger
                     USER        PID ACCESS COMMAND
/home/ubuntu/cpu-logger:
                     ubuntu    32724 ..c.. python
                     ubuntu    32824 ..c.. bash
$ systemctl --user status cpu-logger.service
● cpu-logger.service - CPU logger service
     Loaded: loaded [...]
     Active: active (running) [...]
   Main PID: 32724 (python)

[...]
```

---

```shell
$ fuser -v -m /
                     USER        PID ACCESS COMMAND
/:                   root     kernel mount /
                     ubuntu    32724 .rce. python
                     ubuntu    32824 .rce. bash
$ ls -l /proc/32724/root
[...] /proc/32724/root -> /
$ ls -l /proc/32724/cwd
[...] /proc/32724/cwd -> /home/ubuntu/cpu-logger
$ ls -l /proc/32724/exe
[...] /proc/32724/exe -> /usr/bin/python3.12
```

## 4. File tree layout

Unfortunately
- UNIX systems have never been well organized
- The file tree has many hidden dependencies

As a rule of thumb
- Let everything stay where the OS installation and the system packages put it
- When offered a choice of location, always accept the default unless you have a specific and compelling reason to do otherwise

---

The `hier` man page provides general guidelines for the file tree layout

```shell
$ man hier
```

There is also the [filesystem hierarchy standard](https://refspecs.linuxfoundation.org/FHS_3.0/fhs/index.html) out there, which was last updated in 2015...

In general, don't expect the actual system to conform to the master plan in every respect

---

| Pathname | Contents                                                                                                                                                                                                                        |
| -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `/bin`   | Essential binaries used at boot-time and in single-user mode                                                                                                                                                                    |
| `/boot`  | Boot loader, kernel, and files needed by the kernel                                                                                                                                                                             |
| `/dev`   | Device files                                                                                                                                                                                                                    |
| `/etc`   | Host-specific, system-wide configuration files                                                                                                                                                                                  |
| `/home`  | User home directories                                                                                                                                                                                                           |
| `/lib`   | Essential libraries for the binaries in `/bin` and `/sbin`                                                                                                                                                                      |
| `/media` | Mount points for filesystems on removable media. This directories is for auto-mounted, removable devices                                                                                                                        |
| `/mnt`   | Temporarily mounted filesystems. This is for manual, short-term mounts by system administrators                                                                                                                                 |
| `/opt`   | Optional software packages (rarely used)                                                                                                                                                                                        |
| `/proc`  | Virtual filesystem providing process and kernel information as files                                                                                                                                                            |
| `/root`  | Home directory for the `root` user                                                                                                                                                                                              |
| `/run`   | Temporary filesystem providing run-time variable data. This directory contains system information (e.g., logged-in users, daemons, etc.) since last boot and works as rendezvous for running program (e.g., PID, sockets, etc.) |
| `/sbin`  | Essential binaries used for system administration                                                                                                                                                                               |
| `/srv`   | Site-specific data served by the system (files held for distribution by web servers)                                                                                                                                            |
| `/sys`   | Like `/proc`, filesystem that provides kernel information                                                                                                                                                                       |
| `/tmp`   | Temporary files that may be deleted with no notice, such as by a periodic process or at boot-time                                                                                                                               |
| `/usr`   | Hierarchy of the file tree. This contains the majority of (multi-)user utilities and application. Should be sharable and read-only. Any information that is host-specific or varies over time goes somewhere else               |
| `/var`   | Hierarchy of the file tree. This contains variable data files, i.e., files whose content is expected to continually change during normal operation of the system (e.g., log files)                                              |

## 5. File types

The `file` command determines the type of an existing files (and knows something about common formats used with regular files)

```shell
$ file /var
/var: directory
$ file cpu-logger/app.py
cpu-logger/app.py: Python script, ASCII text executable
$ file cpu-logger/requirements.txt
cpu-logger/requirements.txt: ASCII text
```

---

The `ls` command with the `-l` option shows detailed information about files. The `-d` option forces `ls` to show the information for a directory rather than its contents

```shell
$ ls -l /var
total 44
drwxr-xr-x  2 root root   4096 Mar 28 00:00 backups
drwxr-xr-x 16 root root   4096 Feb  4 11:50 cache

[...]

$ ls -ld /var
drwxr-xr-x 13 root root 4096 Feb  4 10:21 /var
```

---

| File type             | Symbol | Created by          | Removed by |
| --------------------- | ------ | ------------------- | ---------- |
| Regular file          | `-`    | Editors, `cp`, etc. | `rm`       |
| Directory             | `d`    | `mkdir`             | `rm -r`    |
| Symbolic link         | `s`    | `ln -s`             | `rm`       |
| Character device file | `c`    | `mknod`             | `rm`       |
| Block device file     | `b`    | `mknod`             | `rm`       |
| Named pipe            | `p`    | `mkfifo`            | `rm`       |
| Local domain socket   | `s`    | `socket` sys call   | `rm`       |

---

The `rm` command is the universal tool for deleting files

```shell
$ rm <path-to-everything-except-a-dir>
```

```shell
$ mkdir mydir
$ rm mydir
rm: cannot remove 'mydir': Is a directory
$ rm -r mydir
$ echo $?
0
```

---

When `rm` is used in combination with pattern matching, it is a good idea to add the `-i` option, which asks for confirmation before deleting a file

```shell
$ touch file1.txt file2.txt file3.txt
$ rm -i file*
rm: remove regular empty file 'file1.txt'? y
rm: remove regular empty file 'file2.txt'? y
rm: remove regular empty file 'file3.txt'? y
```

### 5.1. Regular files

A file (`-`) that
- Consists of a series of bytes
- Filesystems impose no structure on their contents
- Both sequential access and random access are allowed

Examples are text files, executable programs, etc.

```shell
$ ls -l cpu-logger/
total 8
-rw-rw-r-- 1 ubuntu ubuntu 388 Mar 10 22:01 app.py
-rw-rw-r-- 1 ubuntu ubuntu   7 Mar 10 16:52 requirements.txt
```

### 5.2. Directories

A type of file (`d`) that contains named reference to other files

```shell
ls -la cpu-logger/
total 20
drwxrwxr-x 3 ubuntu ubuntu 4096 Mar 27 15:50 .
drwxr-x--- 7 ubuntu ubuntu 4096 Mar 31 06:58 ..
drwxrwxr-x 5 ubuntu ubuntu 4096 Mar 10 16:57 .venv
-rw-rw-r-- 1 ubuntu ubuntu  388 Mar 10 22:01 app.py
-rw-rw-r-- 1 ubuntu ubuntu    7 Mar 10 16:52 requirements.txt
```

- `.` is a special entry that refers to the directory itself
- `..` is a special entry that refers to the parent directory

### 5.3. Hard links

A directory entry that points to a file

Note that the name of a file is not stored with the file itself, but in a directory entry. Potentially, there may be multiple directory entries that point to the same file. This creates the illusion that a file exists in more than one place at the same time

The `ln` command is to create hard links (same syntax of `cp`)

```shell
$ ln cpu-logger/requirements.txt deleteme
$ cat deleteme
psutil
```

---

```shell
$ ls -i deleteme
327823 deleteme
$ ls -i cpu-logger/requirements.txt
327823 cpu-logger/requirements.txt
```

`327823` is the inode number. An inode is a data structure used by many filesystems to store metadata about a file or a directory. An inode number is just a number to uniquely identify an inode within the system

---

The filesystem maintains a count of the hard links that point to each file

```shell
$ ls -l deleteme
-rw-rw-r-- 2 ubuntu ubuntu 7 Mar 10 16:52 deleteme
```

`2` is the number of hard links that point to the file pointed by `deleteme`. The filesystem does not release the data blocks of a file until the last hard link has been deleted

---

The `find` command with the `-inum` option lists all the hard links in a directory (`$HOME`) for a given inode number (`327823`)

```shell
$ ls -i deleteme
327823 deleteme
$ find $HOME -inum 327823
/home/ubuntu/cpu-logger/requirements.txt
/home/ubuntu/deleteme
```

### 5.4. Symbolic links

A type of file that is a reference by name to another file, i.e., a pathname. Note that symbolic links (aka soft links) may contain pathnames to other filesystems or even to nonexistent files

The `ln` command with the `-s` option creates a symbolic link

```shell
$ ln -s cpu-logger/requirements.txt deleteme
lrwxrwxrwx 1 [...] deleteme -> cpu-logger/requirements.txt
```

---

The file permissions that `ls` shows for a symbolic link (`rwxrwxrwx`) are just dummy values. Permissions on the link target are granted by the target's own permissions. A symbolic link does not have any permission

A common mistake is to think that the first argument to `ln -s` is interpreted relative to the current working directory. The `ln` command does not actually resolve it. This means that the first argument is just a string that becomes the target of the symbolic link

The `readlink` command prints the value of a symbolic link

```shell
$ readlink deleteme
cpu-logger/requirements.txt
```

### 5.5. Character and block device files 

Device files let processes communicate with system hardware and peripherals. The kernel loads the drivers required for each system device. A driver takes care of device management, so the kernel remains relatively hardware-independent

When the filesystem receives a request that refers to a character or block device file, the filesystem passes the request to the appropriate device driver. Device files are just rendezvous points that communicate with device drivers

In the past, device files were manually created in `/dev` with the `mknod` command and removed with the `rm` command. These days, the `/dev` directory is automatically maintained by the kernel in concert with the `udev` daemon

### 5.6 Named pipes

A pipe is a form for inter-process communication that
- Is usually half-duplex (i.e., data flows in only one direction)
- Can only be used between processes that have a common ancestor

```shell
$ grep cat /var/log/auth.log | tail -n 1
[...] COMMAND=/usr/bin/cat /etc/shadow
```

The shell (i.e., the common ancestor) creates a separate process for each command (i.e., `cat` and `grep`) and links the standard output of one process to the standard input of the next using a pipe

---

A named pipe is an extension to the traditional pipe concept. In contrast to a pipe, a named pipe does not require a common ancestor. Named pipes are also called FIFOs because the data written to a named pipe is read in the order it was written. Create a named pipe is similar to creating a file

```shell
$ mkfifo /tmp/mypipe
$ ls -l /tmp/mypipe
prw-rw-r-- 1 ubuntu ubuntu 0 Mar 31 09:27 /tmp/mypipe
$ cat < /tmp/mypipe &
[1] 39875
$ echo "hello" > /tmp/mypipe
hello
[1]+  Done                    cat < /tmp/mypipe
$ rm /tmp/mypipe
```

### 5.7. Local domain sockets

A socket is a form of network inter-process communication. In contrast to pipes, which allow processes running on the same computer to communicate with each other, sockets allow processes to communicate with each other regardless of where they are running

| Domain      | Description          |
| ----------- | -------------------- |
| `AF_INET`   | IPv4 Internet domain |
| `AF_INET6`  | IPv6 Internet domain |
| `AF_UNIX`   | UNIX domain          |
| `AF_UNSPEC` | Unspecified          |

---

| Type             | Description                                                                                                           |
| ---------------- | --------------------------------------------------------------------------------------------------------------------- |
| `SOCK_DGRAM`     | Datagram interface for fixed-length, connectionless, unreliable messages                                              |
| `SOCK_RAW`       | Datagram interface to IP (bypass transport protocols)                                                                 |
| `SOCK_STREAM`    | Sequenced, reliable, bidirectional, connection-oriented byte streams (applications are unaware of message boundaries) |
| `SOCK_SEQPACKET` | Fixed-length, sequenced, reliable, connection-oriented messages (like `SOCK_STREAM`, but a message-based service)     |

---

Local domain sockets (aka UNIX domain sockets) 
- Are full-duplex (while pipes are half-duplex)
- Are used to communicate with processes running on the same computer
- Are more efficient then Internet domain socket because there is no networking overhead (a UNIX domain socket is referred to through a filesystem object rather than a network port)
- Support both stream  (`SOCK_DGRAM`) and datagram (`SOCK_STREAM`) communication (while processes from pipes just read and write bytes)

## 6. File attributes

### 6.1. Permission bits

Nine permission bits determine what operations can be performed on a file and by whom. Three triplets of permission bits define access for the owner (aka user) of the file, the group owners, and everyone else. Each triplet has three bits: a read bit (`r`), a write bit (`w`), and an execute bit (`x`)

Although a user might fit into two of the three permission triplets, only the most specific triplet applies. For example, the owner of a file has always access determined by the owner permission bits and never by the group permission bits

---

| File type | Read bit          | Write bit                                                              | Execute bit |
| --------- | ----------------- | ---------------------------------------------------------------------- | ----------- |
| `-`       | Read              | Write                                                                  | Execute     |
| `d`       | List the contents | Create, delete, and rename files. (works only in combination with `x`) | Enter       |
| `s`       | n/a               | n/a                                                                    | n/a         |
| `c`       | Read              | Write                                                                  | n/a         |
| `b`       | Read              | Write                                                                  | n/a         |
| `p`       | Read              | Write                                                                  | n/a         |
| `s`       | Read              | Connect and write                                                      | n/a         |

---

```shell
$ ls -ld deleteme/
drw-rwxr-x 2 ubuntu ubuntu 4096 Mar 31 19:43 deleteme/
$ ls -l deleteme/
ls: cannot access 'deleteme/file.txt': Permission denied
total 0
-????????? ? ? ? ?            ? file.txt
$ cd deleteme/
-bash: cd: deleteme/: Permission denied
```

### 6.2. Set-UID and set-GID bits

| File type | Set-UID                                             | Set-GID                                                                                                                               |
| --------- | --------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| `-`       | Run an executable file with the owner's permissions | Run an executable file with the group owner's permissions                                                                             |
| `d`       | n/a                                                 | Newly created files take on the group ownership of the directory rather than than the default group of the user that created the file |

The set-GID bit on directories make it easier to share a directory among several users, as long as they belong to a common group

---

```shell
$ ls -l /usr/bin/passwd
-rwsr-xr-x 1 root root 64152 Apr  9  2024 /usr/bin/passwd
$ ls -l /usr/bin/crontab
-rwxr-sr-x 1 root crontab 39664 Mar 31  2024 /usr/bin/crontab
```

When the set-UID (set-GID) is set, `s` replaces the letter `x` in the first (second) triplet. If the set-UID (set-GID) is set but `x` is not, `S` is shown instead of `s`
### 6.3. Sticky bit

The sticky bit applies to directories only. If the sticky bit is set on a directory, a file can only be deleted or renamed by the owner of the directory, the owner of the file, or `root` 

```shell
$ ls -ld /tmp
drwxrwxrwt 12 root root 4096 Mar 31 20:07 /tmp
```

When the sticky bit is set, `t` replaces `x` the third triplet. If the sticky bit is set but `x` is not, `T` is shown instead of `t`

As `/tmp` is shared among users, the sticky bit ensures that a user that is not `root` cannot delete or rename files owned by other users

### 6.4. Listing and inspecting files

```shell
$ ls -l orphan.py
-rw-rw-r-- 1 ubuntu ubuntu 530 Mar 11 13:37 orphan.py
```

| Field          | Meaning                   |
| -------------- | ------------------------- |
| `-`            | File type                 |
| `rw-rw-r--`    | Permission bits           |
| `1`            | Number of hard links      |
| `ubuntu`       | Owner                     |
| `ubuntu`       | Group owner               |
| `530`          | Size of the file in bytes |
| `Mar 11 13:37` | Date of last modification |
| `orphan.py`    | Name of the file          |

---

```shell
$ ls -l /dev/tty0
crw--w---- 1 root tty 4, 0 Mar 20 15:07 /dev/tty0
```

| Field          | Meaning                                                                                                          |
| -------------- | ---------------------------------------------------------------------------------------------------------------- |
| `c`            | File type                                                                                                        |
| `rw--w----`    | Permission bits                                                                                                  |
| `1`            | Number of hard links                                                                                             |
| `root`         | Owner                                                                                                            |
| `tty`          | Group owner                                                                                                      |
| `4`            | Major device number. This identifies the driver that controls the device                                         |
| `0`            | Minor device number. This identifies the device. Note that multiple devices can be controlled by the same driver |
| `Mar 20 15:07` | Date of last modification                                                                                        |
| `/dev/tty0`    | Name of the file                                                                                                 |

### 6.5. Changing permissions

The `chmod` command is to change the permissions on a file. Only the owner and `root` can do it

The first argument of `chmod` is a specification of the permissions to be assigned (either with the octal syntax or the mnemonic syntax), and the following arguments are names of files on which such permissions apply

Bear in mind that a script needs both read and execute permissions turned on, as the interpreter must read the file first. This is not true for binary files, which are directly executed by the kernel. Binary files just need the execute permission

#### 6.5.1. Octal syntax

The octal syntax is generally more convenient for system administrators

However, the octal syntax 
- Can only be used to specify an absolute value for the permission bits. In other words, you cannot just specify one permission bit at a time
- Is more error-prone for people that are not used to octal numbers

| Octal | Binary | Permissions | Additional bits |
| ----- | ------ | ----------- | --------------- |
| `0`   | `000`  | `---`       |                 |
| `1`   | `001`  | `--x`       | Sticky bit      |
| `2`   | `010`  | `-w-`       | Set-GID         |
| `3`   | `011`  | `-wx`       |                 |
| `4`   | `100`  | `r--`       | Set-UID         |
| `5`   | `101`  | `r-x`       |                 |
| `6`   | `110`  | `rw-`       |                 |
| `7`   | `111`  | `rwx`       |                 |

---

```shell
$ chmod 711 myscript
```

- The owner can read, write, and execute (`7` $\rightarrow$ `rwx`)
- The group owner can execute (`1` $\rightarrow$ `--x`)
- The others can execute (`1` $\rightarrow$ `--x`)

To turn on set-UID, set-GID, or sticky bits, use four octal digits rather than three, with the three special bits forming the first digit

```shell
$ chmod 4711 myscript
```

`myscript` has the permission bits set as before and the set-UID is on

#### 6.5.2. Mnemonic syntax

The mnemonic syntax combines a set of targets with an operator and a set of permissions

| Target | Meaning                           |
| ------ | --------------------------------- |
| `u`    | User, i.e., the owner of the file |
| `g`    | Group owner                       |
| `o`    | Other                             |
| `a`    | All, i.e., `ugo`                  |

The mnemonic syntax may be confusing because 
- `o` stands for "other," not "owner" 
- `u` stands for user, which refers to the owner of the file

---

| Operator | Meaning            |
| -------- | ------------------ |
| `+`      | Add permissions    |
| `-`      | Remove permissions |
| `=`      | Set permissions    |

| Permission | Meaning                         |
| ---------- | ------------------------------- |
| `r`        | Read                            |
| `w`        | Write                           |
| `x`        | Execute                         |
| `s`        | Set-UID, set-GID, or sticky bit |

---

```shell
$ chmod u=rwx,g=x,o=x myscript
```

is the equivalent of `711` in octal

```shell
$ chmod u=srwx,g=x,o=x tmp
```

is the equivalent of `4711` in octal

---

| Specification | Meaning                                                                                     |
| ------------- | ------------------------------------------------------------------------------------------- |
| `u+w`         | Add write permission for the owner                                                          |
| `a-x`         | Remove execute permission for all, i.e., owner, group owner, and others                     |
| `ug=rw,o=`    | Set read and write permissions for the owner and group owner, and no permissions for others |
| `g=u`         | Set the permissions for the group owner the same as those of the owner                      |

---

In contrast to the octal syntax, which specifies an absolute value for permissions, the mnemonic syntax preserves permission bits that are set explicitly

```shell
$ ls -l myscript
-r-xr-xr-x 1 ubuntu ubuntu 0 Apr  1 05:42 myscript
$ chmod u+w myscript
$ ls -l myscript
-rwxr-xr-x 1 ubuntu ubuntu 0 Apr  1 05:42 myscript
```

This is particularly useful when the `chmod` command is used with the `-R` option, which recursively updates the file permissions in a directory

---

Bear in mind that the execute bit has a different meaning depending if the target is a regular file or a directory

```shell
$ chmod -R a+x mydir
```

is probably not a good idea. Use `find` to target regular files only

```shell
$ find mydir -type f -exec chmod a-x {} ';'
```

### 6.6. Changing ownership

The `chown` command is to change the ownership of a file. The first argument sets owner and/or group owner (`user:group`), and the following arguments are the files on which the ownership change applies to

Note that a user
- Cannot give away the ownership of a file, except `root`
- Must be the owner of the file and belong to the target group to change group ownership (or just be `root`)

---

```shell
$ ls -l myscript
-rwxr-xr-x 1 ubuntu ubuntu 0 Apr  1 05:42 myscript
$ chown root:root myscript
chown: [...]: Operation not permitted
$ sudo chown root:root myscript
$ ls -l myscript
-rwxr-xr-x 1 root root 0 Apr  1 05:42 myscript
$ sudo chown ubuntu:ubuntu myscript
$ chown :adm myscript
$ ls -l myscript
-rwxr-xr-x 1 ubuntu adm 0 Apr  1 05:42 myscript
```

## Glossary

| Term                                         | Meaning                                                                                                                                                                                                                                                                                   |
| -------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Absolute pathname                            | A pathname that is interpreted starting at `/`                                                                                                                                                                                                                                            |
| Datagram                                     | A self-contained message                                                                                                                                                                                                                                                                  |
| Device file                                  | A type of file that lives in the `/dev` directory that let processes communicate with devices. Requests for a device file are passed to the related device driver                                                                                                                         |
| Directory                                    | A type of file that contains named reference to other files                                                                                                                                                                                                                               |
| File tree                                    | A term used to avoid confusion. The file tree refers to the overall layout. Several filesystems (branches) can be attached to the tree                                                                                                                                                    |
| Filesystem                                   | A structure used by an OS to organize and manage files on a storage device                                                                                                                                                                                                                |
| Fourth extended filesystem (ext4)            | A type of filesystem                                                                                                                                                                                                                                                                      |
| Hard link                                    | A directory entry that points to a file. There may be multiple directory entries that point to the same file. Each file must have at least one hard link                                                                                                                                  |
| Inode                                        | A data structure used by many filesystems to store metadata about a file or a directory                                                                                                                                                                                                   |
| Inode number                                 | A number that uniquely identify an inode within the system                                                                                                                                                                                                                                |
| Local domain socket (aka UNIX domain socket) | A form of inter-process communication. A local domain socket allows processes running un the same computer to communicate with each other. Local domain socket are full-duplex (while pipes are half-duplex) and are more efficient than Internet domain sockets (no networking overhead) |
| Mount point                                  | A directory in the file tree where the root directory of an attached filesystem is mounted. The mount point serves as the entry point for the attached filesystem                                                                                                                         |
| Mounting                                     | Attaching a filesystem to the file tree                                                                                                                                                                                                                                                   |
| Named pipe                                   | A form of inter-process communication. A named pipe is an extension of the traditional pipe concept that does not require a common ancestor                                                                                                                                               |
| Pathname (aka filename or path)              | The list of directories that must be traversed to locate a particular file plus the name of that file                                                                                                                                                                                     |
| Pipe                                         | A form of inter-process communication. A pipe is half-duplex (i.e., data flows in only one direction) and can only be used  between processes that have a common ancestor                                                                                                                 |
| Regular file                                 | A file that consists of a series of bytes. Filesystems impose no structure on the contents of regular files. Both sequential access and random access are allowed. Examples are text files and executable programs                                                                        |
| Relative pathname                            | A pathname that is interpreted starting at the current working directory                                                                                                                                                                                                                  |
| Socket                                       | A form of network inter-process communication. A socket is full-duplex. Sockets allow processes to communicate with each other, regardless of where they are running                                                                                                                      |
| Symbolic link (aka soft link)                | A type of file that is a reference by name to another file. A symbolic link contains a pathname                                                                                                                                                                                           |
| UNIX Filesystems (UFS)                       | A family of filesystems                                                                                                                                                                                                                                                                   |
| Unmounting                                   | Detaching a filesystem to the file tree                                                                                                                                                                                                                                                   |
| XFS                                          | A type of filesystem                                                                                                                                                                                                                                                                      |

## Bibliography 

| Author                   | Title                                                                                                                       | Year |
| ------------------------ | --------------------------------------------------------------------------------------------------------------------------- | ---- |
| Bach, M.                 | [The Design of the UNIX Operating System](https://dl.acm.org/doi/10.5555/8570)                                              | 1986 |
| Kerrisk, M.              | [The Linux Programming Interface](https://man7.org/tlpi)                                                                    | 2010 |
| Stevens, R. and Rago, S. | [Advanced Programming in the UNIX Environment](https://www.oreilly.com/library/view/advanced-programming-in/9780321638014/) | 2013 |
| Nemeth, E. et al.        | [UNIX and Linux System Administration Handbook](https://www.admin.com/)                                                     | 2018 |
| Community                | [Wikipedia](https://en.wikipedia.org/)                                                                                      | 2025 |

## Licenses

| Content | License                                                                                                                       |
| ------- | ----------------------------------------------------------------------------------------------------------------------------- |
| Code    | [MIT License](https://mit-license.org/)                                                                                       |
| Text    | [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International](https://creativecommons.org/licenses/by-nc-sa/4.0/) |
