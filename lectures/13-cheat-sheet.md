# Cheat sheet

## Booting and system management daemons

| Command         | Meaning                                |
| --------------- | -------------------------------------- |
| `efibootmgr`    | Change UEFI boot manager configuration |
| `grup-mkconfig` | Generate GRUB configuration file       |
| `systemctl`     | Control `systemd`                      |
| `update-grub`   | Stub for `grub-mkconfig`               |

## Access control and rootly powers

| Command               | Meaning                                                       |
| --------------------- | ------------------------------------------------------------- |
| `cat`                 | Concatenate files and print on the stdout                     |
| `echo`                | Display a line of text                                        |
| `grep`                | Print lines that match patterns                               |
| `head`                | Output the first part of files                                |
| `id`                  | Print real and effective user and group IDs                   |
| `ls`                  | List directory contents                                       |
| `passwd`              | Change user password                                          |
| `su`                  | Allows commands to be run with a substitute user and group ID |
| `sudo`                | Execute a command as another user                             |
| `tail`                | Output the last part of files                                 |
| `update-alternatives` | Maintain symbolic links determining default commands          |
| `which`               | Locate a command                                              |
| `whoami`              | Print effective user name                                     |

## Process control

| Command           | Meaning                                                          |
| ----------------- | ---------------------------------------------------------------- |
| `du`              | Estimate file space usage                                        |
| `kill`            | Send a signal to a process                                       |
| `nice`            | Run a program with modified scheduling priority                  |
| `pgrep`           | Find the process IDs that match the selection criteria to stdout |
| `pidof`           | Find the process ID of a running program                         |
| `ps`              | Report a snapshot of the current processes                       |
| `renice`          | Alter priority of running processes                              |
| `strace`          | Trace system calls and signals                                   |
| `systemd-analyze` | Analyze and debug `systemd`                                      |
| `top`             | Provide a dynamic real-time view of a running system             |

## The filesystem

| Command    | Meaning                                               |
| ---------- | ----------------------------------------------------- |
| `chmod`    | Change file permission bits                           |
| `chown`    | Change file owner and group                           |
| `file`     | Determine file type                                   |
| `find`     | Search for files in a directory hierarchy             |
| `fuser`    | Identify processes using files or sockets             |
| `ln`       | Make links between files                              |
| `man`      | Show manual pages                                     |
| `mkdir`    | Make directories                                      |
| `mkfifo`   | Make FIFOs (named pipes)                              |
| `mount`    | Mount a filesystem                                    |
| `pwd`      | Print name of current working directory               |
| `readlink` | Print resolved symbolic links or canonical file names |
| `rm`       | Remove files                                          |
| `touch`    | Change file timestamps                                |
| `umount`   | Unmount a filesystem                                  |

## Networking

| Command      | Meaning                                                                        |
| ------------ | ------------------------------------------------------------------------------ |
| `apt`        | Command-line interface for the package management system                       |
| `ip`         | Show and manipulate routing, network devices, interfaces and tunnels           |
| `ipcalc`     | Calculate broadcast, network, wildcard mask, and host range of an IPv4 address |
| `iperf3`     | Perform network throughput tests                                               |
| `ping`       | Send ICMP echo request to network hosts                                        |
| `sysctl`     | Configure kernel parameters at runtime                                         |
| `tcpdump`    | Dump traffic on a network                                                      |
| `traceroute` | Print the route packets trace to network host                                  |

## Security

| Command       | Meaning                                                                             |
| ------------- | ----------------------------------------------------------------------------------- |
| `iptables`    | Administer IPv4 packet filtering and NAT                                            |
| `john`        | Crack passwords                                                                     |
| `lsof`        | List open files                                                                     |
| `nmap`        | Perform network exploration, security auditing, and port scanning                   |
| `scp`         | Copy files between hosts on a network using SFTP                                    |
| `sftp`        | Provide an interactive experience similar to a traditional FTP client but over SFTP |
| `sftp-server` | Run server for file transfer over SFTP                                              |
| `shasum`      | Print or check SHA checksums                                                        |
| `ss`          | Dump socket statistics                                                              |
| `ssh`         | Run SSH client                                                                      |
| `ssh-add`     | Add private key identities to `ssh-agent`                                           |
| `ssh-agent`   | Run SSH authentication agent                                                        |
| `ssh-keygen`  | Generate public/private key pairs                                                   |
| `ssh-keyscan` | Retrieve public keys from servers                                                   |
| `sshd`        | Run SSH server daemon                                                               |
| `unshadow`    | Combine `etc/passwd` and `/etc/shadow`                                              |

## Appendixes

### Subcommands

#### apt

| Subcommand | Argument  | Meaning                                                  |
| ---------- | --------- | -------------------------------------------------------- |
| `update`   | n/a       | Download package information from all configured sources |
| `install`  | `package` | Install `package`                                        |

#### ip

| Subcommand | Argument | Meaning                |
| ---------- | -------- | ---------------------- |
| `route`    | n/a      | Show routing table     |
| `neigh`    | n/a      | Show ARP cache entries |

#### systemctl

| Subcommand        | Argument  | Meaning                                                        |
| ----------------- | --------- | -------------------------------------------------------------- |
| `daemon-reload`   | n/a       | Reload unit files and `systemd` config                         |
| `disable`         | `unit`    | Prevent `unit` from activating at boot                         |
| `enable`          | `unit`    | Enable `unit` to activate at boot                              |
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

#### systemd-analyze

| Subcommand | Argument     | Meaning                                                                                                         |
| ---------- | ------------ | --------------------------------------------------------------------------------------------------------------- |
| `calendar` | `expression` | Parse a calendar repetitive event `expression`, output the normalized form, and calculate when next occurrences |
| `timespan` | `expression` | Parse a time span `expression` and output the normalized form and the equivalent value in microseconds          |

### Signal codes

| #   | Name   | Description      | Default   | Dump | Catch | Block |
| --- | ------ | ---------------- | --------- | ---- | ----- | ----- |
| 1   | `HUP`  | Hangup           | Terminate | No   | Yes   | Yes   |
| 2   | `INT`  | Interrupt        | Terminate | No   | Yes   | Yes   |
| 3   | `QUIT` | Quit             | Terminate | Yes  | Yes   | Yes   |
| 9   | `KILL` | Kill             | Terminate | No   | No    | No    |
| 10  | `BUS`  | Bus error        | Terminate | Yes  | Yes   | Yes   |
| 11  | `SEGV` | Segm. fault      | Terminate | Yes  | Yes   | Yes   |
| 15  | `TERM` | Software term.   | Terminate | No   | Yes   | Yes   |
| 17  | `STOP` | Stop             | Stop      | No   | No    | No    |
| 18  | `TSTP` | Keyboard stop    | Stop      | No   | Yes   | Yes   |
| 19  | `CONT` | Cont. after stop | Ignore    | No   | Yes   | No    |
| 30  | `USR1` | User-defined 1   | Terminate | No   | Yes   | Yes   |
| 31  | `USR2` | User-defined 2   | Terminate | No   | Yes   | Yes   |

### IPv4 

#### Address classes

| Class | 1st byte      | Implicit netmask        | Use case               |
| ----- | ------------- | ----------------------- | ---------------------- |
| A     | `0` - `127`   | `255.0.0.0` (`/8`)      | Large networks         |
| B     | `128` - `191` | `255.255.0.0` (`/16`)   | Medium networks        |
| C     | `192` - `223` | `255.255.255.0` (`/24`) | Small networks         |
| D     | `224` - `239` | n/a                     | Multicasting           |
| E     | `240` - `255` | n/a                     | Experimental addresses |

#### Private addresses

| IP class | From          | To                | CIDR range       |
| -------- | ------------- | ----------------- | ---------------- |
| A        | `10.0.0.0`    | `10.255.255.255`  | `10.0.0.0/8`     |
| B        | `172.16.0.0`  | `172.31.255.255`  | `172.16.0.0/12`  |
| C        | `192.168.0.0` | `192.168.255.255` | `192.168.0.0/16` |
