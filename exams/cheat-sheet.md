# Cheat sheet

- [1. Basics](#1-basics)
    - [1.1. Signal codes](#11-signal-codes)
- [2. System and service management](#2-system-and-service-management)
    - [2.1. systemctl](#21-systemctl)
    - [2.2. systemd-analyze](#22-systemd-analyze)
- [3. Account administration](#3-account-administration)
    - [3.1. Root privileges](#31-root-privileges)
    - [3.2. Users and groups](#32-users-and-groups)
- [4. Container management](#4-container-management)
    - [4.1. podman](#41-podman)
- [5. Network configuration](#5-network-configuration)
    - [5.1. ip](#51-ip)
    - [5.2. IPv4](#52-ipv4)
        - [5.2.1. Address classes](#521-address-classes)
        - [5.2.2. Private addresses](#522-private-addresses)
- [6. Manual pages](#6-manual-pages)

## 1. Basics

| Command    | Meaning                                               |
| ---------- | ----------------------------------------------------- |
| `cat`      | Concatenate files and print on the stdout             |
| `cd`       | Change working directory                              |
| `chmod`    | Change file permission bits                           |
| `chown`    | Change file owner and group                           |
| `cp`       | Copy files                                            |
| `du`       | Estimate file space usage                             |
| `echo`     | Display a line of text                                |
| `file`     | Determine file type                                   |
| `find`     | Search for files in a directory hierarchy             |
| `grep`     | Print lines that match patterns                       |
| `head`     | Output the first part of files                        |
| `id`       | Print real and effective user and group IDs           |
| `kill`     | Send a signal to a process                            |
| `less`     | Display file contents one screen at a time            |
| `ln`       | Make links between files                              |
| `ls`       | List directory contents                               |
| `man`      | Show manual pages                                     |
| `mkdir`    | Make directories                                      |
| `mv`       | Move (rename) files                                   |
| `nano`     | Text editor                                           |
| `ps`       | Report a snapshot of the current processes            |
| `pwd`      | Print name of current working directory               |
| `python3`  | CPython, version 3                                    |
| `readlink` | Print resolved symbolic links or canonical file names |
| `rm`       | Remove files                                          |
| `sleep`    | Delay for a specified amount of time                  |
| `tail`     | Output the last part of files                         |
| `top`      | Provide a dynamic real-time view of a running system  |
| `vim`      | Text editor                                           |
| `which`    | Locate a command                                      |
| `whoami`   | Print effective user name                             |

### 1.1. Signal codes

| #   | Name   | Description      | Default   | Dump | Catch | Block |
| --- | ------ | ---------------- | --------- | ---- | ----- | ----- |
| 1   | `HUP`  | Hangup           | Terminate | No   | Yes   | Yes   |
| 2   | `INT`  | Interrupt        | Terminate | No   | Yes   | Yes   |
| 3   | `QUIT` | Quit             | Terminate | Yes  | Yes   | Yes   |
| 7   | `BUS`  | Bus error        | Terminate | Yes  | Yes   | Yes   |
| 9   | `KILL` | Kill             | Terminate | No   | No    | No    |
| 10  | `USR1` | User-defined 1   | Terminate | No   | Yes   | Yes   |
| 11  | `SEGV` | Segm. fault      | Terminate | Yes  | Yes   | Yes   |
| 12  | `USR2` | User-defined 2   | Terminate | No   | Yes   | Yes   |
| 15  | `TERM` | Software term.   | Terminate | No   | Yes   | Yes   |
| 18  | `CONT` | Cont. after stop | Ignore    | No   | Yes   | No    |
| 19  | `STOP` | Stop             | Stop      | No   | No    | No    |
| 20  | `TSTP` | Keyboard stop    | Stop      | No   | Yes   | Yes   |

## 2. System and service management

| Command           | Meaning                                    |
| ----------------- | ------------------------------------------ |
| `journalctl`      | Print log entries from the systemd journal |
| `systemctl`       | Control `systemd`                          |
| `systemd-analyze` | Analyze and debug `systemd`                |

### 2.1. systemctl

| Subcommand        | Argument  | Meaning                                                        |
| ----------------- | --------- | -------------------------------------------------------------- |
| `daemon-reload`   | n/a       | Reload unit files and `systemd` config                         |
| `disable`         | `unit`    | Prevent `unit` from activating at boot                         |
| `enable`          | `unit`    | Enable `unit` to activate at boot                              |
| `get-default`     | n/a       | Show the default target                                        |
| `isolate`         | `target`  | Change operating mode to `target`                              |
| `kill`            | `pattern` | Send a signal to units matching `pattern`                      |
| `list-timers`     | `pattern` | List the timer units matching `pattern` currently in memory    |
| `list-unit-files` | `pattern` | List the unit files matching `pattern` installed in the system |
| `list-units`      | `pattern` | List the units matching `pattern` currently in memory          |
| `reboot`          | n/a       | Reboot the computer                                            |
| `restart`         | `unit`    | Restart `unit` immediately                                     |
| `start`           | `unit`    | Activate `unit` immediately                                    |
| `status`          | `unit`    | Show the status of `unit` and recent logs                      |
| `stop`            | `unit`    | Deactivate `unit` immediately                                  |

### 2.2. systemd-analyze

| Subcommand | Argument     | Meaning                                                                                                         |
| ---------- | ------------ | --------------------------------------------------------------------------------------------------------------- |
| `calendar` | `expression` | Parse a calendar repetitive event `expression`, output the normalized form, and calculate when next occurrences |
| `timespan` | `expression` | Parse a time span `expression` and output the normalized form and the equivalent value in microseconds          |

## 3. Account administration

### 3.1. Root privileges

| Command  | Meaning                                                       |
| -------- | ------------------------------------------------------------- |
| `su`     | Allows commands to be run with a substitute user and group ID |
| `sudo`   | Execute a command as another user                             |
| `visudo` | Edit the sudoers file with syntax validation                  |

### 3.2. Users and groups

| Command    | Meaning                             |
| ---------- | ----------------------------------- |
| `chage`    | Change user password-aging metadata |
| `groupadd` | Create a new group                  |
| `groupdel` | Remove a group                      |
| `passwd`   | Change user password                |
| `useradd`  | Create a new user account           |
| `userdel`  | Remove a user account               |
| `usermod`  | Modify an existing user account     |
| `vipw`     | Edit the password file with locking |

## 4. Container management

| Command   | Meaning                         |
| --------- | ------------------------------- |
| `podman`  | Manage containers and images    |

### 4.1. podman

| Subcommand    | Argument    | Meaning                                        |
| ------------- | ----------- | ---------------------------------------------- |
| `build`       | n/a         | Build an image from a Containerfile            |
| `exec`        | `container` | Run a command in running `container`           |
| `image prune` | n/a         | Discard images not referenced by any container |
| `images`      | n/a         | List locally stored images                     |
| `ps`          | n/a         | Show running containers                        |
| `pull`        | `image`     | Pull `image` from a registry                   |
| `push`        | `image`     | Push `image` to a registry                     |
| `rm`          | `container` | Remove stopped `container`                     |
| `rmi`         | `image`     | Remove `image`                                 |
| `run`         | `image`     | Create and start a container from `image`      |
| `start`       | `container` | Start stopped `container`                      |
| `stop`        | `container` | Stop running `container`                       |
| `tag`         | `image`     | Add a name and tag to `image`                  |

## 5. Network configuration

| Command      | Meaning                                                               |
| ------------ | --------------------------------------------------------------------- |
| `ip`         | Show and manipulate routing, network devices, interfaces, and tunnels |
| `iptables`   | Administer IPv4 packet filtering and NAT                              |
| `nc`         | Open arbitrary TCP or UDP connections                                 |
| `ping`       | Send ICMP echo request to network hosts                               |
| `ss`         | Dump socket statistics                                                |
| `sysctl`     | Configure kernel parameters at runtime                                |
| `tcpdump`    | Dump traffic on a network                                             |
| `traceroute` | Print the route packets trace to network host                         |

### 5.1. ip

| Subcommand | Argument | Meaning                          |
| ---------- | -------- | -------------------------------- |
| `address`  | n/a      | Show network interface addresses |
| `neigh`    | n/a      | Show ARP cache entries           |
| `route`    | n/a      | Show routing table               |

### 5.2. IPv4

#### 5.2.1. Address classes

| Class | 1st byte      | Implicit netmask        | Use case               |
| ----- | ------------- | ----------------------- | ---------------------- |
| A     | `0` - `127`   | `255.0.0.0` (`/8`)      | Large networks         |
| B     | `128` - `191` | `255.255.0.0` (`/16`)   | Medium networks        |
| C     | `192` - `223` | `255.255.255.0` (`/24`) | Small networks         |
| D     | `224` - `239` | n/a                     | Multicasting           |
| E     | `240` - `255` | n/a                     | Experimental addresses |

#### 5.2.2. Private addresses

| IP class | From          | To                | CIDR range       |
| -------- | ------------- | ----------------- | ---------------- |
| A        | `10.0.0.0`    | `10.255.255.255`  | `10.0.0.0/8`     |
| B        | `172.16.0.0`  | `172.31.255.255`  | `172.16.0.0/12`  |
| C        | `192.168.0.0` | `192.168.255.255` | `192.168.0.0/16` |

## 6. Manual pages

| Page                         | Topic                                         |
| ---------------------------- | --------------------------------------------- |
| `man:systemd.unit(5)`        | `[Unit]` and `[Install]` section directives   |
| `man:systemd.service(5)`     | `[Service]` section directives                |
| `man:systemd.timer(5)`       | `[Timer]` directives and calendar expressions |
| `man:sudoers(5)`             | Sudoers file syntax                           |
| `man:iptables(8)`            | `iptables` command-line syntax                |
| `man:iptables-extensions(8)` | `iptables` match modules (e.g., `conntrack`)  |

## Licenses

| Content | License                                                                                                                       |
| ------- | ----------------------------------------------------------------------------------------------------------------------------- |
| Code    | [MIT License](https://mit-license.org/)                                                                                       |
| Text    | [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International](https://creativecommons.org/licenses/by-nc-sa/4.0/) |
