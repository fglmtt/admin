# Mock exam

## Table of contents

- [1. Daemon](#1-daemon)
    - [1.1. Python script](#11-python-script)
    - [1.2. Service](#12-service)
    - [1.3. Solution](#13-solution)
- [2. Account administration](#2-account-administration)
    - [2.1. Text](#21-text)
    - [2.2. Solution](#22-solution)
- [Licenses](#licenses)

## 1. Daemon

### 1.1. Python script

Write a Python script that periodically analyzes a specified directory (including all its subdirectories), identifying files whose size exceeds or equals a certain threshold (in bytes). Whenever the script finds a file whose size is greater than or equal to the threshold, it must write the file's path to a log file. In your home directory, create a directory called `large-file-detector`, and inside it, the file `app.py`, using this template:

```python
# first name and last name:
# student id:
#
# path:

import argparse
import os
import sys
import time

def main():
    pass


if __name__ == "__main__":
    main()
```

The script must accept exactly four mandatory command-line arguments, parsed with the `argparse` module: `--target`, indicating the absolute path of the directory to check; `--size`, specifying the minimum size in bytes (positive integer) of files to report; `--interval`, defining the interval in seconds (positive integer) between each check; and finally, `--log`, specifying where to save the log file. The log file's name is always `large-file-detector.log`.

After parsing, validate the received inputs: check that the path specified by `--target` is absolute (`os.path.isabs`), exists (`os.path.exists`), and is a directory (`os.path.isdir`); also check that the values provided for `--size` and `--interval` are positive integers; verify that the path indicated by `--log` exists (`os.path.exists`) and is a directory (`os.path.isdir`).

After validation, recursively traverse the directory tree at the path provided with `--target` (`os.listdir`, `os.path.join`, `os.path.isdir`). For each file (`os.path.isfile`), compute its size (`os.path.getsize`) and compare it with the threshold defined by `--size`. If the size is greater than or equal to the indicated threshold, write the absolute path of the file, followed by a newline, into the log file named `large-file-detector.log` (`open`), located in the directory specified with `--log`. Each write operation to the log file must be in append mode. The script must repeat this procedure periodically, waiting a number of seconds equal to the value indicated by `--interval` between each check (`time.sleep`).

For example, running

```shell
$ python ~/large-file-detector/app.py \
    --target ~/archive \
    --size 10 \
    --interval 30 \
    --log ~
```

the script will identify all files of `10` bytes or more in `~/archive` (and all its subdirectories) and append the path of each identified file to `~/large-file-detector.log`. The script will repeat this operation every `30` seconds.

### 1.2. Service

Create a service unit named `large-file-detector.service` in your user's `systemd` instance. The unit must start `~/large-file-detector/app.py` with the arguments `--target %h/docs`, `--size 100`, `--interval 300`, and `--log %h`, start at system boot, and restart in case of failures. Use this template:

```
# first name and last name:
# student id:
#
# path: 
# 
# command to enable the service:
# command to start the service:
```

### 1.3. Solution

This exercise was proposed on [June 20, 2025](https://github.com/fglmtt/admin/tree/main/exams/2025-06-20/large-file-detector).

## 2. Account administration

### 2.1. Text

Configure `sudo` on a fleet of four Linux hosts: three cache hosts (`cache01`, `cache02`, `cache03`) and a gateway host (`gateway01`). The fleet has the following users and groups:

| User     | Primary group | Additional groups |
| -------- | ------------- | ----------------- |
| `liam`   | `liam`        |                   |
| `mia`    | `mia`         | `ops`             |
| `noah`   | `noah`        | `ops`             |
| `olivia` | `olivia`      | `audit`           |

Apply the following rules:

| Category    | Rule                                                                                                                                                          |
| ----------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Aliases     | Define `Host_Alias CACHE = cache01, cache02, cache03`                                                                                                         |
| Aliases     | Define `Cmnd_Alias SHELLS = /bin/sh, /bin/dash, /bin/bash`, `Cmnd_Alias NETMGM = /usr/bin/ss, /usr/bin/ip`, and `Cmnd_Alias BACKUP = /usr/bin/rsync, /usr/bin/tar` |
| Permissions | `liam` can run any command as any user on any host                                                                                                            |
| Permissions | `mia` can run any command as any user on any host, except `SHELLS`                                                                                            |
| Permissions | `%ops` can run `NETMGM` as `root` on `CACHE`                                                                                                                  |
| Permissions | `%audit` can run `BACKUP` as `root` on `gateway01`, without a password                                                                                        |
| Permissions | `noah` can run `/usr/bin/tail -f /var/log/syslog` as `root` on any host, without a password                                                                   |
| Permissions | `olivia` can run `/usr/bin/id` as `mia` on `CACHE`                                                                                                            |
| Permissions | `%ops, %audit` can run `/usr/sbin/reboot` as `root` on any host, without a password                                                                           |

The file must be created at `/etc/sudoers.d/local`. Use this template:

```
# first name and last name:
# student id:
#
# path:
```

### 2.2. Solution

```
# first name and last name: mattia fogli
# student id: 123456
#
# path: /etc/sudoers.d/local

Host_Alias  CACHE = cache01, cache02, cache03

Cmnd_Alias  SHELLS  = /bin/sh, /bin/dash, /bin/bash
Cmnd_Alias  NETMGM  = /usr/bin/ss, /usr/bin/ip
Cmnd_Alias  BACKUP  = /usr/bin/rsync, /usr/bin/tar

liam            ALL       = (ALL) ALL
mia             ALL       = (ALL) ALL, !SHELLS
%ops            CACHE     = NETMGM
%audit          gateway01 = NOPASSWD: BACKUP
noah            ALL       = NOPASSWD: /usr/bin/tail -f /var/log/syslog
olivia          CACHE     = (mia) /usr/bin/id
%ops, %audit    ALL       = NOPASSWD: /usr/sbin/reboot
```

## Licenses

| Content | License                                                                                                                       |
| ------- | ----------------------------------------------------------------------------------------------------------------------------- |
| Code    | [MIT License](https://mit-license.org/)                                                                                       |
| Text    | [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International](https://creativecommons.org/licenses/by-nc-sa/4.0/) |
