# The filesystem

## Table of contents

- [1. Bad and good news](#1-bad-and-good-news)
- [2. Pathnames](#2-pathnames)
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
    - [6.4. Changing permissions](#64-changing-permissions)
    - [6.5. Changing ownership](#65-changing-ownership)
- [Glossary](#glossary)
- [Bibliography](#bibliography)
- [Licenses](#licenses)

## 1. Bad and good news

A filesystem comprises four main components: a namespace for naming and organizing objects in a hierarchy, an application programming interface (API) for navigating and manipulating those objects, a security model for protecting and sharing them, and an implementation that ties the logical model to the hardware.

Modern kernels define an abstract interface that accommodates many different implementations. Disk-based filesystems live on local storage. Network filesystems are handled by drivers that forward operations to another computer. Pseudo filesystems expose kernel state as files. Every object reachable through the filesystem is accessed through the same API. Hence the UNIX mantra: everything is a file.

The unification is leaky, however. Device files, for example, are rendezvous points for drivers, not data files — yet they live in the filesystem and carry on-disk metadata like regular files. Special cases like these make the result look like a Frankenstein's monster.

## 2. Pathnames

The filesystem is a single unified hierarchy that starts at the root directory `/` and continues downward through an arbitrary number of subdirectories. A pathname is the list of directories that must be traversed to locate a particular file and the name of that file.

Pathnames can be either absolute or relative. Relative pathnames are interpreted starting at the current working directory (use `cd` to change the shell working directory). Absolute pathnames are interpreted starting at `/`.

The terms filenames, pathnames, and path are more or less interchangeable.

## 3. Mounting and unmounting

The filesystem is composed of smaller chunks, which are also called filesystems. Each of these consists of one directory and its subdirectories and files.

Henceforth, the term file tree will refer to the overall layout. The term filesystem will be reserved to the "branches" attached to the tree.

A filesystem can be anything that obeys the proper API, from a disk partition to a network file server or a kernel component.

### 3.1. Mounting

In most situations, filesystems are attached to the tree with the `mount` command. `mount` maps a directory within the existing file tree, called the mount point, to the root of the newly attached filesystem.

The previous contents of the mount point become temporarily inaccessible as long as another filesystem is mounted there. However, mount points are usually empty directories. For example

```shell
$ mount /dev/sda4 /mnt
```

mounts the filesystem stored on the disk partition `/dev/sda4` under the path `/mnt` in the file tree.

### 3.2. Unmounting

The `umount` command is to detach filesystems from the file tree. A filesystem can be unmounted if there are no

- Open files
- Processes whose current directories are located there
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

The `umount` command also provides a lazy unmount option (`umount -l`) that removes a filesystem from the naming hierarchy but does not truly unmount it until all existing file references have been closed.

> [!warning]
> - There is no guarantee that existing references will ever close on their own
> - Lazy unmounted filesystems present inconsistent semantics to the programs that are using them. For example, programs can read and write open files but cannot open new files

---

When a filesystem is busy, a good idea is to find out which processes hold references to that filesystem. The `fuser` command with the `-m` option prints who is using a mounted filesystem

```shell
$ sudo fuser -v -m /proc
            USER        PID ACCESS COMMAND
/proc:      root     kernel mount /proc
            root          1 f.... systemd
            root        281 f.... systemd-journal
            root        641 f.... udisksd
            syslog      675 f.... rsyslogd
            ubuntu    32713 f.... systemd
```

- the kernel has mounted `/proc`
- `systemd` (`PID 1`) has an open file (`f`) in `/proc`

## 4. File tree layout

The `hier` man page provides general guidelines for the file tree layout. There is also the [Filesystem Hierarchy Standard](https://refspecs.linuxfoundation.org/FHS_3.0/fhs/index.html) out there, which was last updated in 2015...

In general, don't expect the actual system to conform to the master plan in every respect.

> [!tip]
> As a rule of thumb
> - As the file tree has many hidden dependencies, let everything stay where the OS installation and the system packages put it
> - When offered a choice of location, always accept the default unless you have a specific and compelling reason to do otherwise

## 5. File types

| File type             | Symbol | Created by          | Removed by |
| --------------------- | ------ | ------------------- | ---------- |
| Regular file          | `-`    | Editors, `cp`, etc. | `rm`       |
| Directory             | `d`    | `mkdir`             | `rm -r`    |
| Symbolic link         | `l`    | `ln -s`             | `rm`       |
| Character device file | `c`    | `mknod`             | `rm`       |
| Block device file     | `b`    | `mknod`             | `rm`       |
| Named pipe            | `p`    | `mkfifo`            | `rm`       |
| Local domain socket   | `s`    | `socket` sys call   | `rm`       |

### 5.1. Regular files

A regular file (`-`) consists of a series of bytes. Filesystems impose no structure on their contents. Both sequential access and random access are allowed.

Examples are text files, executable programs, etc.

```shell
$ ls -l cpu-logger/
total 8
-rw-rw-r-- 1 ubuntu ubuntu 388 Mar 10 22:01 app.py
-rw-rw-r-- 1 ubuntu ubuntu   7 Mar 10 16:52 requirements.txt
```

### 5.2. Directories

A directory (`d`) is a type of file that contains named references to other files.

```shell
$ ls -la cpu-logger/
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

A hard link is a directory entry that points to a file.

The name of a file is not stored with the file itself but in a directory entry, so multiple directory entries can point to the same file. This creates the illusion that a file exists in more than one place.

The `ln` command creates a hard link (same syntax as `cp`)

```shell
$ ln cpu-logger/requirements.txt deleteme
```

---

```shell
$ ls -i cpu-logger/requirements.txt deleteme
327823 cpu-logger/requirements.txt
327823 deleteme
```

- `-i` prints the inode number
- `327823` is the inode number

The two names share the same inode number. Since inode numbers are only unique within a single filesystem, hard links cannot cross filesystem boundaries.

---

The filesystem maintains a count of the hard links that point to each file (the second column of `ls -l`)

```shell
$ ls -l deleteme
-rw-rw-r-- 2 ubuntu ubuntu 7 Mar 10 16:52 deleteme
```

As the filesystem does not release the data blocks until the last hard link is removed, locating the remaining links is sometimes necessary

```shell
$ find $HOME -inum 327823
/home/ubuntu/cpu-logger/requirements.txt
/home/ubuntu/deleteme
```

### 5.4. Symbolic links

A symbolic link (`l`), also known as a soft link, is a type of file that is a reference by name to another file, i.e., a pathname. Symbolic links may contain pathnames to other filesystems or even to nonexistent files.

The `ln` command with the `-s` option creates a symbolic link

```shell
$ ln -s cpu-logger/requirements.txt deleteme
$ ls -l
lrwxrwxrwx 1 [...] deleteme -> cpu-logger/requirements.txt
```

---

The file permissions that `ls` shows for a symbolic link (`rwxrwxrwx`) are just dummy values. Permissions on the link target are granted by the target's own permissions. A symbolic link does not have any permissions.

A symbolic link stores its target as a literal string. That string is resolved at access time, relative to the directory containing the link — not relative to the working directory at the time `ln -s` was invoked. The `readlink` command prints the value of a symbolic link

```shell
$ readlink deleteme
cpu-logger/requirements.txt
```

### 5.5. Character and block device files

A device file (`c` for character, `b` for block) lets processes communicate with system hardware and peripherals. The kernel loads the drivers required for each system device. A driver takes care of device management, so the kernel remains relatively hardware-independent.

When the filesystem receives a request that refers to a character or block device file, the filesystem passes the request to the appropriate device driver. Device files are just rendezvous points that communicate with device drivers.

In the past, device files were manually created in `/dev` with the `mknod` command and removed with the `rm` command. These days, the `/dev` directory is automatically maintained by the kernel in concert with the `udev` daemon.

### 5.6. Named pipes

A pipe is a form of inter-process communication that

- Is usually half-duplex (i.e., data flows in only one direction)
- Can only be used between processes that have a common ancestor

```shell
$ cat /var/log/auth.log | tail -n 1
[...] COMMAND=/usr/bin/cat /etc/shadow
```

The shell (i.e., the common ancestor) creates a separate process for each command (i.e., `cat` and `tail`) and links the standard output of one process to the standard input of the next using a pipe

---

A named pipe (`p`) is an extension to the traditional pipe concept. In contrast to a pipe, a named pipe does not require a common ancestor. Named pipes are also called FIFOs because the data written to a named pipe is read in the order it was written. Creating a named pipe is similar to creating a file

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

A socket (`s`) is a form of inter-process communication that allows processes to communicate with each other regardless of where they are running.

Sockets have two attributes: a domain and a type. The domain selects the addressing scheme, while the type selects the communication semantics. For example, a stream socket in the IPv4 domain is a TCP socket: reliable and connection-oriented.

Local domain sockets are restricted to processes running on the same host and are referred to through a filesystem object rather than a network port. They are full-duplex (unlike pipes), support both stream and datagram communication, and are more efficient than Internet domain sockets because they bypass the networking stack.

## 6. File attributes

### 6.1. Permission bits

| File type | `r`               | `w`                                                                   | `x`     |
| --------- | ----------------- | --------------------------------------------------------------------- | ------- |
| `-`       | Read              | Write                                                                 | Execute |
| `d`       | List the contents | Create, delete, and rename files (works only in combination with `x`) | Enter   |
| `l`       | n/a               | n/a                                                                   | n/a     |
| `c`       | Read              | Write                                                                 | n/a     |
| `b`       | Read              | Write                                                                 | n/a     |
| `p`       | Read              | Write                                                                 | n/a     |
| `s`       | Read              | Connect and write                                                     | n/a     |

### 6.2. Set-UID and set-GID bits

| File type | Set-UID                                             | Set-GID                                                                                                                          |
| --------- | --------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| `-`       | Run an executable file with the owner's permissions | Run an executable file with the group owner's permissions                                                                        |
| `d`       | n/a                                                 | Newly created files take on the group ownership of the directory rather than the default group of the user that created the file |

> [!tip]
> The set-GID bit on directories makes it easier to share a directory among several users, as long as they belong to a common group.

### 6.3. Sticky bit

The sticky bit applies to directories only. If the sticky bit is set on a directory, a file can only be deleted or renamed by the owner of the directory, the owner of the file, or `root`. When the sticky bit is set, `t` replaces `x` in the third triplet

```shell
$ ls -ld /tmp
drwxrwxrwt 12 root root 4096 Mar 31 20:07 /tmp
```

> [!note]
> As `/tmp` is shared among users, the sticky bit ensures that a user that is not `root` cannot delete or rename files owned by other users.

### 6.4. Changing permissions

The `chmod` command is to change the permissions on a file.

> [!note]
> Only the owner and `root` can do it.

The first argument of `chmod` is a specification of the permissions to be assigned (either with the octal syntax or the mnemonic syntax), and the following arguments are names of files on which such permissions apply

---

The octal syntax packs the three permission triplets into three octal digits, with an optional fourth leading digit for the set-UID, set-GID, and sticky bits.

For example

```shell
$ chmod 755 myscript
```

- `7` (owner): read, write, execute
- `5` (group owner): read and execute
- `5` (others): read and execute

> [!warning]
> The octal syntax is absolute: every invocation sets all permission bits. You cannot change one bit without specifying the others.

---

The mnemonic syntax combines a set of targets (`u`, `g`, `o`, `a`) with an operator (`+`, `-`, `=`) and a set of permissions (`r`, `w`, `x`, `s`, `t`).

In contrast to the octal syntax, which specifies an absolute value for permissions, the mnemonic syntax preserves permission bits that are not set explicitly

```shell
$ ls -l myscript
-r-xr-xr-x 1 ubuntu ubuntu 0 Apr  1 05:42 myscript
$ chmod u+w myscript
$ ls -l myscript
-rwxr-xr-x 1 ubuntu ubuntu 0 Apr  1 05:42 myscript
```

---

This is particularly useful when the `chmod` command is used with the `-R` option, which recursively updates the file permissions in a directory. However, the execute bit has a different meaning depending on whether the target is a regular file or a directory

```shell
$ chmod -R a+x mydir
```

is probably not a good idea. Use `find` to target regular files only

```shell
$ find mydir -type f -exec chmod a-x {} ';'
```

### 6.5. Changing ownership

The `chown` command is to change the ownership of a file. The first argument sets owner and/or group owner (`user:group`), and the following arguments are the files to which the ownership change applies.

> [!note]
> A user
> - Cannot give away the ownership of a file (only `root` can)
> - Must be the owner of the file and belong to the target group to change group ownership (or just be `root`)

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
| Device file                                  | A type of file that lives in the `/dev` directory that lets processes communicate with devices. Requests for a device file are passed to the related device driver                                                                                                                         |
| Directory                                    | A type of file that contains named references to other files                                                                                                                                                                                                                              |
| File tree                                    | A term used to avoid confusion. The file tree refers to the overall layout. Several filesystems (branches) can be attached to the tree                                                                                                                                                    |
| Filesystem                                   | A structure used by an OS to organize and manage files. Implementations range from disk partitions to network file servers and kernel-provided pseudo filesystems                                                                                                                          |
| Hard link                                    | A directory entry that points to a file. There may be multiple directory entries that point to the same file. Each file must have at least one hard link                                                                                                                                  |
| Inode                                        | A data structure used by many filesystems to store metadata about a file or a directory                                                                                                                                                                                                   |
| Inode number                                 | A number that uniquely identifies an inode within a filesystem                                                                                                                                                                                                                              |
| Local domain socket (aka UNIX domain socket) | A form of inter-process communication. A local domain socket allows processes running on the same computer to communicate with each other. Local domain sockets are full-duplex (while pipes are half-duplex) and are more efficient than Internet domain sockets (no networking overhead) |
| Mount point                                  | A directory in the file tree where the root directory of an attached filesystem is mounted. The mount point serves as the entry point for the attached filesystem                                                                                                                         |
| Mounting                                     | Attaching a filesystem to the file tree                                                                                                                                                                                                                                                   |
| Named pipe                                   | A form of inter-process communication. A named pipe is an extension of the traditional pipe concept that does not require a common ancestor                                                                                                                                               |
| Pathname (aka filename or path)              | The list of directories that must be traversed to locate a particular file plus the name of that file                                                                                                                                                                                     |
| Permission bits                              | Nine bits that define who can access a file or directory and what actions they can perform                                                                                                                                                                                                |
| Pipe                                         | A form of inter-process communication. A pipe is half-duplex (i.e., data flows in only one direction) and can only be used between processes that have a common ancestor                                                                                                                  |
| Regular file                                 | A file that consists of a series of bytes. Filesystems impose no structure on the contents of regular files. Both sequential access and random access are allowed. Examples are text files and executable programs                                                                        |
| Relative pathname                            | A pathname that is interpreted starting at the current working directory                                                                                                                                                                                                                  |
| Set-GID                                      | A special permission bit. On an executable, it causes the process to run with the effective GID of the file's group owner. On a directory, it causes newly created files to inherit the group ownership of the directory                                                                  |
| Set-UID                                      | A special permission bit that causes an executable to run with the effective UID of the file's owner rather than the invoking user                                                                                                                                                        |
| Socket                                       | A form of inter-process communication. A socket is full-duplex. Sockets allow processes to communicate with each other, regardless of where they are running                                                                                                                              |
| Sticky bit                                   | A special permission bit for directories. When set, a file in the directory can only be deleted or renamed by the owner of the directory, the owner of the file, or `root`                                                                                                               |
| Symbolic link (aka soft link)                | A type of file that is a reference by name to another file. A symbolic link contains a pathname                                                                                                                                                                                           |
| Unmounting                                   | Detaching a filesystem from the file tree                                                                                                                                                                                                                                                   |

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
