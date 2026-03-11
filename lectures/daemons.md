# Daemons

## Table of contents

- [1. Text](#1-text)
    - [1.1. Python script](#11-python-script)
    - [1.2. Service](#12-service)
- [2. Hints](#2-hints)
    - [2.1. System reference manuals](#21-system-reference-manuals)
    - [2.2. Python script](#22-python-script)
        - [2.2.1. Program execution](#221-program-execution)
        - [2.2.2. Interactive mode](#222-interactive-mode)
        - [2.2.3. Documentation](#223-documentation)
        - [2.2.4. Program structure](#224-program-structure)
        - [2.2.5. Recursion](#225-recursion)
    - [2.3. Service](#23-service)
        - [2.3.1. Unit file structure](#231-unit-file-structure)
        - [2.3.2. Unit file location](#232-unit-file-location)
        - [2.3.3. Service management](#233-service-management)
        - [2.3.4. Logs](#234-logs)
- [3. Solution](#3-solution)
- [Licenses](#licenses)

## 1. Text

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

```ini
# first name and last name:
# student id:
#
# path:
#
# command to enable the service:
# command to start the service:
```

## 2. Hints

### 2.1. System reference manuals

`man` displays the system reference manuals. For example, `man:systemctl(1)` translates to

```shell
$ man 1 systemctl
```

### 2.2. Python script

#### 2.2.1. Program execution

To run a Python program

```shell
$ python3 <your_program>.py
```

> [!warning]
> Depending on your system, you may have to use `python` or `python3`.

#### 2.2.2. Interactive mode

The interactive mode starts a read-eval-print loop (REPL) where you can type Python expressions and see their results immediately. This is useful for experimenting with functions and modules before writing a full program.

To enable the interactive mode

```shell
$ python3
```

#### 2.2.3. Documentation

`help()` displays documentation for modules, functions, classes, and keywords in the Python interactive interpreter. For example, to read the documentation for the `argparse` module

```shell
$ python3
>>> import argparse
>>> help(argparse)
```

To get help on a specific function

```shell
$ python3
>>> import os.path
>>> help(os.path.isabs)
```

#### 2.2.4. Program structure

The following extends the template from [§1.1](#11-python-script) with comments that map to each step described in the text.

```python
# first name and last name:
# student id:
#
# path:

import argparse
import os
import sys
import time


def walk(basepath, size, log_path):
    # recursive traversal
    pass


def main():
    # argument parsing

    # validation

    # periodic execution
    pass


if __name__ == "__main__":
    main()
```

#### 2.2.5. Recursion

The following example recursively lists all file paths in a directory tree.

```python
import os


def walk(basepath):
    for filename in os.listdir(basepath):
        path = os.path.join(basepath, filename)
        if os.path.isfile(path):
            print(path)
        elif os.path.isdir(path):
            walk(path)
```

### 2.3. Service

#### 2.3.1. Unit file structure

The following extends the template from [§1.2](#12-service) with comments that map to each section of the unit file.

```ini
# first name and last name:
# student id:
#
# path:
#
# command to enable the service:
# command to start the service:

[Unit]
# human-readable description

[Service]
# how to run the service
# what to do on failure

[Install]
# start on boot
```

An example of a service unit file is provided [here](https://github.com/fglmtt/admin/blob/main/lectures/booting-and-system-management-daemons.md#21-units-and-unit-files). The available directives are documented in `man:systemd.unit(5)` (for `[Unit]` and `[Install]`) and `man:systemd.service(5)` (for `[Service]`).

> [!tip]
> `%h` expands to the home directory of the user running the service. For example, `WorkingDirectory=%h/large-file-detector` expands to `WorkingDirectory=/home/ubuntu/large-file-detector`.

> [!tip]
> Add `Environment=PYTHONUNBUFFERED=1` to `[Service]` so that `print` output shows up in `journalctl` right away.

#### 2.3.2. Unit file location

The directories where `systemd` reads unit files are documented in `man:systemd.unit(5)`. The recommended directory for user units is `~/.config/systemd/user`. If it does not exist, create it

```shell
$ mkdir -p ~/.config/systemd/user
```

Then copy the unit file there

```shell
$ cp ~/large-file-detector/large-file-detector.service ~/.config/systemd/user
```

#### 2.3.3. Service management

The commands to control `systemd` are listed [here](https://github.com/fglmtt/admin/blob/main/lectures/booting-and-system-management-daemons.md#22-controlling-systemd). Append the `--user` option to control the user instance instead of the system-wide one. See also `man:systemctl(1)`.

After copying the unit file:

- [ ] List unit files to verify that `systemd` sees the new file (`list-unit-files`)
- [ ] Reload unit files so that `systemd` picks up any changes (`daemon-reload`)
- [ ] Start the service (`start`)
- [ ] Check the status to confirm it was correctly loaded and is running (`status`)
- [ ] Enable the service so it starts on boot (`enable`)
- [ ] Reboot the system
- [ ] Check the status to confirm it survived the reboot (`status`)
- [ ] Kill the service to simulate a failure (`kill`)
- [ ] Check the status to confirm `systemd` restarted it (`status`)

> [!tip]
> Use `systemctl --user kill --signal=SIGKILL large-file-detector.service` to forcefully kill your service and verify that `systemd` restarts it.

#### 2.3.4. Logs

`journalctl` queries the `systemd` journal. Append the `--user` option to read logs from the user instance. For example

```shell
$ journalctl --user -u large-file-detector.service
```

See also `man:journalctl(1)`.

## 3. Solution

This exercise was proposed on [June 20, 2025](https://github.com/fglmtt/admin/tree/main/exams/2025-06-20/large-file-detector).

## Licenses

| Content | License                                                                                                                       |
| ------- | ----------------------------------------------------------------------------------------------------------------------------- |
| Code    | [MIT License](https://mit-license.org/)                                                                                       |
| Text    | [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International](https://creativecommons.org/licenses/by-nc-sa/4.0/) |
