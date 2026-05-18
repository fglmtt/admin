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

Write a Python script that periodically calculates the total size of all files in a specified directory (including all its subdirectories) and logs the date, time, and total size when it exceeds a given threshold expressed in bytes. In your home directory, create the directory `dir-size-monitor` and, inside it, the file `app.py`, using this template:

```python
# first and last name:
# student id:
#
# path:

import argparse
from datetime import datetime
import os
import sys
import time

def main():
    pass


if __name__ == "__main__":
    main()
```

The script must accept exactly four mandatory command-line arguments, parsed with the `argparse` module: `--target`, which specifies the absolute path of the directory to monitor; `--threshold`, which specifies the threshold in bytes (positive integer) above which a warning must be logged; `--interval`, which defines the interval in seconds (positive integer) between each check; and `--log`, which specifies the absolute path of the directory where to save the log file. The name of the log file is always `dir-size-monitor.log`.

After parsing, validate the received inputs: verify that the path specified with `--target` is absolute (`os.path.isabs`), that it exists (`os.path.exists`), and that it is a directory (`os.path.isdir`); also check that the values provided for `--threshold` and `--interval` are positive integers; verify that the path indicated with `--log` exists, that is a directory, and that is absolute. If any check fails, print an explanatory error message to standard error (`print`) and exit with a non-zero status code (`sys.exit`).

After validation, recursively traverse the directory tree at the path provided with `--target` (`os.listdir`, `os.path.join`, `os.path.isdir`). For each file encountered (`os.path.isfile`), get its size (`os.path.getsize`) and add it to an accumulator to calculate the total size of the directory. If the total size is greater than or equal to the threshold indicated by `--threshold`, open in append mode the log file `dir-size-monitor.log` in the directory specified with `--log` (`open`) and write a line containing the current date and time (`datetime.now`), a space, and the total size in bytes. The script must repeat this procedure periodically, waiting for a number of seconds equal to the value indicated by `--interval` between each check (`time.sleep`).

For example, running:

```shell
$ python ~/dir-size-monitor/app.py \
    --target ~/documents \
    --threshold 1000 \
    --interval 60 \
    --log ~
```

the script will calculate the total size of all files in `~/documents` (and in all its subdirectories) and, if that size is greater than or equal to `1000` bytes, will append to `~/dir-size-monitor.log` the date, time, and total size. The script will repeat the operation every `60` seconds.

### 1.2. Service

Create a service unit named `dir-size-monitor.service` in your user instance of `systemd`. The unit must start `~/dir-size-monitor/app.py` with the arguments `--target %h/documents`, `--threshold 1000`, `--interval 60`, and `--log %h`, start at system boot, and restart in case of failures. Use this template:

```
# first and last name:
# student id:
#
# path:
#
# command to enable the service:
# command to start the service:
```

### 1.3. Solution

This exercise was proposed on [February 9, 2026](https://github.com/fglmtt/admin/tree/main/exams/2026-02-09/dir-size-monitor).

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
