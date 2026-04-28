# Account administration

## Table of contents

- [1. Text](#1-text)
- [2. Hints](#2-hints)
    - [2.1. System reference manuals](#21-system-reference-manuals)
    - [2.2. Sudoers file](#22-sudoers-file)
        - [2.2.1. File structure](#221-file-structure)
        - [2.2.2. File location](#222-file-location)
    - [2.3. Testing](#23-testing)
        - [2.3.1. Container](#231-container)
        - [2.3.2. Users and groups](#232-users-and-groups)
        - [2.3.3. Verification](#233-verification)
- [3. Solution](#3-solution)
- [Licenses](#licenses)

## 1. Text

Configure `sudo` on a fleet of four Linux hosts: two web hosts (`web01`, `web02`) and two database hosts (`db01`, `db02`). The fleet has the following users and groups:

| User    | Primary group | Additional groups |
| ------- | ------------- | ----------------- |
| `alice` | `alice`       |                   |
| `bob`   | `bob`         |                   |
| `carol` | `carol`       | `ops`             |
| `dave`  | `dave`        | `devs`            |

Apply the following rules:

| Category    | Rule                                                                                                                                                                                 |
| ----------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Aliases     | Define `Host_Alias WEB = web01, web02` and `Host_Alias DB = db01, db02`                                                                                                              |
| Aliases     | Define `Cmnd_Alias SHELLS = /bin/sh, /bin/dash, /bin/bash`, `Cmnd_Alias USERMGM = /usr/sbin/useradd, /usr/sbin/userdel, /usr/sbin/usermod`, and `Cmnd_Alias PKGINFO = /usr/bin/dpkg` |
| Permissions | `alice` can run any command as any user on any host                                                                                                                                  |
| Permissions | `bob` can run any command as any user on any host, except `SHELLS`                                                                                                                   |
| Permissions | `%ops` can run `USERMGM` as `root` on `WEB`                                                                                                                                          |
| Permissions | `%devs` can run `PKGINFO` as `root` on `DB`, without a password                                                                                                                      |
| Permissions | `carol` can run `/usr/bin/cat /etc/shadow` as `root` on any host, without a password                                                                                                 |
| Permissions | `dave` can run `/usr/bin/id` as `nobody` on `DB`                                                                                                                                     |
| Permissions | `%ops, %devs` can run `/usr/sbin/reboot` as `root` on any host, without a password                                                                                                   |

The file must be created at `/etc/sudoers.d/local`. Use this template:

```
# first name and last name:
# student id:
#
# path:
```

## 2. Hints

### 2.1. System reference manuals

`man` displays the system reference manuals. For example, `man:sudoers(5)` translates to

```shell
$ man 5 sudoers
```

See also `man:sudo(8)` and `man:visudo(8)`.

### 2.2. Sudoers file

#### 2.2.1. File structure

A [sudoers file](https://github.com/fglmtt/admin/blob/main/lectures/access-control-and-rootly-powers.md#232-the-sudoers-file) contains aliases and permission lines. A permission line has the shape

```
<who> <where> = (<as whom>) [NOPASSWD:] <what>
```

where

- `<who>` is a user or group
- `<where>` is one or more hosts
- `<as whom>` is the target user(s)
- `<what>` is one or more commands

The complete syntax reference is in `man:sudoers(5)`.

#### 2.2.2. File location

The recommended drop-in directory for additional sudoers files is `/etc/sudoers.d/`. The `/etc/sudoers` file ends with `@includedir /etc/sudoers.d`, so every file in that directory is appended to the live configuration in lexicographic order.

> [!warning]
> If you are working on a lab machine, you cannot create a file in `/etc/sudoers.d/`.

> [!tip]
> Edit the file on your machine with any text editor — it does not need to live under `/etc/sudoers.d/` to be syntax-checked.
> 
> `visudo -c -f <path>` parses a sudoers file without opening an editor or modifying the live configuration. It prints `parsed OK` and exits with status 0 when the file is valid; otherwise it points at the offending line.

### 2.3. Testing

#### 2.3.1. Container

Use [`podman`](https://github.com/fglmtt/admin/blob/main/lectures/containers.md#3-podman) to run the course's container image (`fglmtt/admin`). First, pull the image

```shell
$ podman pull fglmtt/admin
```

Then, run a container. For example

```shell
$ podman run \
    -d \
    --name web01 \
    --hostname web01 \
    -v </path/to/your/sudoers>:/tmp/local:ro \
    fglmtt/admin \
    sleep infinity
```

- `-d` runs the container in the background
- `--name web01` assigns a name to the container
- `--hostname web01` sets the hostname for the container
- `-v </path/to/your/sudoers>:/tmp/local:ro` mounts the candidate sudoers file read-only at `/tmp/local`
- `fglmtt/admin` is the image
- `sleep infinity` keeps the container alive so that `podman exec` can attach to it

To open a shell inside the `web01` container

```shell
$ podman exec -it web01 bash
```

Re-run the pattern with a different `--hostname` and a different `--name` to exercise host-scoped rules. Multiple containers can run side by side.

Install the file inside the container

```shell
$ sudo cp /tmp/local /etc/sudoers.d
$ sudo chmod 0440 /etc/sudoers.d/local
```

> [!warning]
> `sudo` refuses to read sudoers files that are writable by anyone other than `root` or not owned by `root`, so set ownership to `root:root` and permissions to `0440`.

#### 2.3.2. Users and groups

The `fglmtt/admin` image only ships the `ubuntu` user, which has broad access to `sudo`. Create the required users and groups inside containers before testing (see [this](https://github.com/fglmtt/admin/blob/main/lectures/user-management.md) for user and group management commands).

For example

```shell
$ sudo groupadd <group>
$ sudo useradd -m <user>
$ sudo passwd <user>
$ sudo usermod -aG <group> <user>
```

> [!tip]
> To actually exercise a rule, become the user with `su -l <user>`.

#### 2.3.3. Verification

On your machine

- [ ] Run `visudo -c -f <path>` to confirm the candidate sudoers file parses

Spin up four containers, one per hostname (`web01`, `web02`, `db01`, `db02`). In each container

- [ ] Install the sudoers file at `/etc/sudoers.d/local`
- [ ] Run `visudo -c` to confirm `sudo` accepts the installed file
- [ ] Create users and groups

Then, for each rule

- [ ] Open a shell on a container whose hostname matches the rule
- [ ] Become the user with `su -l <user>`, then run `sudo -l` to confirm the rule appears in the listing
- [ ] Run a command the rule should allow and confirm it succeeds, with or without a password prompt as expected
- [ ] Run a variant the rule should refuse — the same command from a different host, or a command outside the rule — and confirm `sudo` refuses it (if applicable)

> [!tip]
> `sudo -k` clears the cached credential. Run it between checks to re-observe password-prompt behavior.

> [!tip]
> To run a command as a specific user, use `sudo -u <user> <command>`. To also set the primary group, add `-g <group>`.

## 3. Solution

```
# first name and last name: mattia fogli
# student id: 123456
#
# path: /etc/sudoers.d/local

Host_Alias  WEB = web01, web02
Host_Alias  DB  = db01, db02

Cmnd_Alias  SHELLS   = /bin/sh, /bin/dash, /bin/bash
Cmnd_Alias  USERMGM  = /usr/sbin/useradd, /usr/sbin/userdel, /usr/sbin/usermod
Cmnd_Alias  PKGINFO  = /usr/bin/dpkg

alice        ALL = (ALL) ALL
bob          ALL = (ALL) ALL, !SHELLS
%ops         WEB = USERMGM
%devs        DB  = NOPASSWD: PKGINFO
carol        ALL = NOPASSWD: /usr/bin/cat /etc/shadow
dave         DB  = (nobody) /usr/bin/id
%ops, %devs  ALL = NOPASSWD: /usr/sbin/reboot
```

## Licenses

| Content | License                                                                                                                       |
| ------- | ----------------------------------------------------------------------------------------------------------------------------- |
| Code    | [MIT License](https://mit-license.org/)                                                                                       |
| Text    | [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International](https://creativecommons.org/licenses/by-nc-sa/4.0/) |
