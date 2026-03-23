# Periodic processes

## Table of contents

- [1. Text](#1-text)
    - [1.1. Python script](#11-python-script)
    - [1.2. Service](#12-service)
    - [1.3. Timer](#13-timer)
- [2. Hints](#2-hints)
    - [2.1. System reference manuals](#21-system-reference-manuals)
    - [2.2. Python script](#22-python-script)
        - [2.2.1. Program execution](#221-program-execution)
        - [2.2.2. Interactive mode](#222-interactive-mode)
        - [2.2.3. Documentation](#223-documentation)
        - [2.2.4. Program structure](#224-program-structure)
        - [2.2.5. Recursion](#225-recursion)
        - [2.2.6. String matching](#226-string-matching)
    - [2.3. Service](#23-service)
        - [2.3.1. Unit file structure](#231-unit-file-structure)
        - [2.3.2. Unit file location](#232-unit-file-location)
        - [2.3.3. Service management](#233-service-management)
        - [2.3.4. Logs](#234-logs)
    - [2.4. Timer](#24-timer)
        - [2.4.1. Unit file structure](#241-unit-file-structure)
        - [2.4.2. Unit file location](#242-unit-file-location)
        - [2.4.3. Timer verification](#243-timer-verification)
        - [2.4.4. Timer management](#244-timer-management)
- [3. Solution](#3-solution)
- [Licenses](#licenses)

## 1. Text

### 1.1. Python script

Write a Python script that analyzes log files in a specified directory and its subdirectories, extracting lines that contain a specified string and writing them to output files in a backup directory named `backup`, created (if necessary) in `~`. In your home directory, create a directory called `log-extractor` and, within it, a file named `app.py`, using this template:

```python
# first and last name:
# student id:
#
# path:

import argparse
import os
import sys

def main():
    pass


if __name__ == "__main__":
    main()
```

The script must accept exactly two command-line arguments, parsed using the `argparse` module. The first argument, `--path`, is a mandatory string specifying the absolute path of the directory to analyze. The second argument, `--pattern`, is a mandatory string specifying the pattern to search for within log files, i.e., those files with a `.log` extension.

After parsing, validate both inputs: check that the path is absolute (`os.path.isabs`), exists (`os.path.exists`), and is a directory (`os.path.isdir`); verify that `--pattern` is a non-empty string. If any check fails, print an explanatory error message to standard error (`print`) and exit with a non-zero status code (`sys.exit`).

After validation, ensure the `backup` directory exists in `~` (`os.path.expanduser`, `os.makedirs`). Recursively traverse the directory tree at the provided path (`os.listdir`, `os.path.join`, `os.path.isdir`). For each log file encountered (`os.path.isfile`, `str.endswith`), check if it contains the specified pattern by reading its content (`open`). If the pattern is found, extract the corresponding lines and write them to a file with the same name in the `~/backup` directory (`open`, `file.writelines`), printing a log message to standard output (`print`) indicating the number of lines written and the destination file name.

For example, running:

```shell
$ python ~/log-extractor/app.py \
    --path ~/logs \
    --pattern ERROR
```

the script will extract all lines containing the string `ERROR` from files with a `.log` extension in `~/logs` and its subdirectories, writing them to corresponding files in the `~/backup` folder.

### 1.2. Service

Create a service unit named `log-extractor.service` in your user instance of `systemd`. Configure it to run `~/log-extractor/app.py` with the arguments `--path %h/logs` and `--pattern ERROR`. Use this template:

```ini
# first and last name:
# student id:
#
# path:
```

### 1.3. Timer

Create a timer unit named `log-extractor.timer` in your user instance of `systemd`. Configure it to activate `log-extractor.service` every Monday and Friday at 02:00. Use this template:

```ini
# first and last name:
# student id:
#
# path:
#
# command to enable the timer:
# command to start the timer:
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


def find(filename, pattern):
    # read file, return matching lines
    pass


def dump(filename, lines):
    # write lines to file
    pass


def walk(log_dir, backup_dir, pattern):
    # recursive traversal
    pass


def main():
    # argument parsing

    # validation

    # ensure backup directory exists

    # scan
    pass


if __name__ == "__main__":
    main()
```

> [!tip]
> `os.makedirs` raises `FileExistsError` if the directory already exists. Pass `exist_ok=True` to silently skip creation when the directory is already there.

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

#### 2.2.6. String matching

The following example reads all lines from a file and keeps only those that contain a given string.

```python
with open("server.log", "r") as f:
    lines = f.readlines()

matching = [line for line in lines if "timeout" in line]
```

### 2.3. Service

#### 2.3.1. Unit file structure

The following extends the template from [§1.2](#12-service) with comments that map to each section of the unit file.

```ini
# first name and last name:
# student id:
#
# path:

[Unit]
# human-readable description

[Service]
# how to run the service
```

An example of a service unit file is provided [here](https://github.com/fglmtt/admin/blob/main/lectures/booting-and-system-management-daemons.md#21-units-and-unit-files). The available directives are documented in `man:systemd.unit(5)` (for `[Unit]`) and `man:systemd.service(5)` (for `[Service]`).

> [!tip]
> `%h` expands to the home directory of the user running the service. For example, `WorkingDirectory=%h/log-extractor` expands to `WorkingDirectory=/home/ubuntu/log-extractor`.

> [!tip]
> Add `Environment=PYTHONUNBUFFERED=1` to `[Service]` so that `print` output shows up in `journalctl` right away.

> [!warning]
> This service unit file does not have an `[Install]` section. The timer unit is responsible for activating the service, so the service does not need to be enabled or started on boot independently.

#### 2.3.2. Unit file location

The directories where `systemd` reads unit files are documented in `man:systemd.unit(5)`. The recommended directory for user units is `~/.config/systemd/user`. If it does not exist, create it

```shell
$ mkdir -p ~/.config/systemd/user
```

Then copy the unit file there

```shell
$ cp ~/log-extractor/log-extractor.service ~/.config/systemd/user
```

#### 2.3.3. Service management

The commands to control `systemd` are listed [here](https://github.com/fglmtt/admin/blob/main/lectures/booting-and-system-management-daemons.md#22-controlling-systemd). Append the `--user` option to control the user instance instead of the system-wide one. See also `man:systemctl(1)`.

After copying the unit file:

- [ ] List unit files to verify that `systemd` sees the new file (`list-unit-files`)
- [ ] Inspect the unit file to verify its content (`cat`)
- [ ] Reload unit files so that `systemd` picks up any changes (`daemon-reload`)
- [ ] Start the service (`start`)
- [ ] Check the status to confirm it ran correctly (`status`)

#### 2.3.4. Logs

`journalctl` queries the `systemd` journal. Append the `--user` option to read logs from the user instance. For example

```shell
$ journalctl --user -u log-extractor.service
```

See also `man:journalctl(1)`.

### 2.4. Timer

#### 2.4.1. Unit file structure

The following extends the template from [§1.3](#13-timer) with comments that map to each section of the unit file.

```ini
# first name and last name:
# student id:
#
# path:
#
# command to enable the timer:
# command to start the timer:

[Unit]
# human-readable description

[Timer]
# which service to activate
# schedule (calendar expression)

[Install]
# start on boot
```

The available directives are documented in `man:systemd.timer(5)` (for `[Timer]`) and `man:systemd.unit(5)` (for `[Unit]` and `[Install]`). The timer types and calendar expressions are covered [here](https://github.com/fglmtt/admin/blob/main/lectures/process-control.md#7-periodic-processes).

#### 2.4.2. Unit file location

Timer unit files go in the same directory as service unit files: `~/.config/systemd/user`.

```shell
$ cp ~/log-extractor/log-extractor.timer ~/.config/systemd/user
```

#### 2.4.3. Timer verification

`systemd-analyze calendar` parses calendar time events and calculates when they elapse next. Use it to verify your `OnCalendar` expression before deploying the timer.

```shell
$ systemd-analyze calendar 'Wed *-*-* 14:00' --iterations=3
  Original form: Wed *-*-* 14:00
Normalized form: Wed *-*-* 14:00:00
    Next elapse: Wed 2025-05-21 14:00:00 UTC
       From now: 1 day left
   Iteration #2: Wed 2025-05-28 14:00:00 UTC
       From now: 8 days left
   Iteration #3: Wed 2025-06-04 14:00:00 UTC
       From now: 15 days left
```

See [here](https://github.com/fglmtt/admin/blob/main/lectures/process-control.md#72-time-expressions) for more on time expressions.

#### 2.4.4. Timer management

After copying the unit file:

- [ ] List unit files to verify that `systemd` sees the new file (`list-unit-files`)
- [ ] Inspect the unit file to verify its content (`cat`)
- [ ] Reload unit files so that `systemd` picks up any changes (`daemon-reload`)
- [ ] Start the timer (`start`)
- [ ] Check the status to confirm it is active and waiting (`status`)
- [ ] List active timers to see the next trigger time (`list-timers`)
- [ ] Enable the timer so it starts on boot (`enable`)
- [ ] Reboot the system
- [ ] Check the status to confirm it survived the reboot (`status`)

## 3. Solution

This exercise was proposed on [September 8, 2025](https://github.com/fglmtt/admin/tree/main/exams/2025-09-08/log-extractor).

## Licenses

| Content | License                                                                                                                       |
| ------- | ----------------------------------------------------------------------------------------------------------------------------- |
| Code    | [MIT License](https://mit-license.org/)                                                                                       |
| Text    | [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International](https://creativecommons.org/licenses/by-nc-sa/4.0/) |
