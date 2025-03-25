# Access control and rootly powers

## Table of contents

- [1. Access control](#1-access-control)
    - [1.1. Access control v. security](#11-access-control-v-security)
    - [1.2. Standard UNIX access control](#12-standard-unix-access-control)
        - [1.2.1. Filesystem access control](#121-filesystem-access-control)
        - [1.2.2. Process ownership](#122-process-ownership)
        - [1.2.3. The root account](#123-the-root-account)
        - [1.2.4. Set-UID execution](#124-set-uid-execution)
- [2. Rootly powers](#2-rootly-powers)
    - [2.1. Root account login](#21-root-account-login)
    - [2.2. Substituting user identities](#22-substituting-user-identities)
    - [2.3. Executing commands as another user](#23-executing-commands-as-another-user)
        - [2.3.1. Logs](#231-logs)
        - [2.3.2. The sudoers file](#232-the-sudoers-file)
        - [2.3.3. Permission precedence](#233-permission-precedence)
        - [2.3.4. Editing permissions](#234-editing-permissions)
    - [2.4. Final remarks](#24-final-remarks)
        - [2.4.1. Pros and cons of sudo](#241-pros-and-cons-of-sudo)
        - [2.4.2. Best practices](#242-best-practices)
- [Glossary](#glossary)
- [Bibliography](#bibliography)
- [Licenses](#licenses)

## 1. Access control

### 1.1. Access control v. security

Access control 
- How the kernel and its delegates make security-related decisions

Security
- How to set up a system or network to minimize the chance of unwelcome access by intruders

### 1.2. Standard UNIX access control

The standard UNIX access control model has remained largely unchanged for decades. This model follows a few basic rules
1. Access control decisions depend on which user (or, in some cases, the user's membership in a group) is attempting to perform an operation
2. Objects have owners. Files and processes are examples of objects. Owners have broad, but not necessarily unrestricted, control over their objects
3. You own the objects you create
4. The special user account `root` can act as the owner of any object
5. Only `root` can perform certain sensitive administrative operations

#### 1.2.1. Filesystem access control

Every file has both an owner and a group (aka group owner)
- The owner can set the permissions of the file
- The owner is always a single person
- Many people can be group owners, as long as they are in the group

```shell
$ ls -l hello.txt
-rw-rw-r-- 1 ubuntu ubuntu 6 Mar  4 10:36 hello.txt
```

---

`hello.txt` is owned by user `ubuntu` (first) and group `ubuntu` (second)

| Permission bits | Meaning                                             |
| --------------- | --------------------------------------------------- |
| `-`             | `hello.txt` is a regular file                       |
| `rw-`           | The owner (`ubuntu`) can read (`r`) and write (`w`) |
| `rw-`           | The group (`ubuntu`) can read (`r`) and write (`w`) |
| `r--`           | The others can read (`r`)                           |

---

The kernel tracks owners and groups as numbers rather than as text names

If you do not know your (effective) user name

```shell
$ whoami
ubuntu
```

UIDs are mapped to usernames in `/etc/passwd`

```shell
$ cat /etc/passwd | grep ubuntu
ubuntu:x:1000:1000:Ubuntu:/home/ubuntu:/bin/bash
```

---

| Field          | Meaning                                                                       |
| -------------- | ----------------------------------------------------------------------------- |
| `ubuntu`       | Username                                                                      |
| `x`            | Password placeholder. The actual password is stored in the `/etc/shadow` file |
| `1000`         | UID                                                                           |
| `1000`         | GID                                                                           |
| `Ubuntu`       | Comment field (optional)                                                      |
| `/home/ubuntu` | Home directory                                                                |
| `/bin/bash`    | Default shell                                                                 |

---

GIDs are mapped to group names in `/etc/group`

```shell
$ cat /etc/group | grep ubuntu | head -n 1
adm:x:4:syslog,ubuntu
```

| Field           | Meaning                                                                        |
| --------------- | ------------------------------------------------------------------------------ |
| `adm`           | Group name                                                                     |
| `x`             | Password placeholder. The actual password, if any, is stored in `/etc/gshadow` |
| `4`             | GID                                                                            |
| `syslog,ubuntu` | List of users that belong to `adm`                                             |

#### 1.2.2. Process ownership

The owner of a process can
- Send process signals
- Reduce process scheduling priority

There are multiple identities associated with a process

| Identity                                    | Meaning                                 |
| ------------------------------------------- | --------------------------------------- |
| real UID and GID                            | Who we really are                       |
| Effective UID and GID<br>Supplementary GIDs | Used for file access permission checks  |
| Saved IDs                                   | Used to enter and leave privileged mode |

---

Real UID and GID
- Are taken from `/etc/passwd` on login
- Do not typically change during a login session (`root` could do it)

Effective UID, effective GID, and supplementary GIDs
- Determine the actual file access permissions

Saved IDs
- Saved set-UID contains a copy of the effective UID
- Saved set-GID contains a copy of the effective GID

---

When a program is executed
- Real UID = UID of the user who ran the command
- Real GID = GID of the user who ran the command

Typically
- Real UID = effective UID
- Real GID = effective GID

---

```shell
$ id
uid=1000(ubuntu) gid=1000(ubuntu) groups= [...]
$ which sleep
/usr/bin/sleep
$ ls -l /usr/bin/sleep
-rwxr-xr-x [...] root root [...] /usr/bin/sleep
$ sleep 10 &
[1] 14766
$ ps -o pid,ruid,euid,suid,cmd | grep sleep
14766  1000  1000  1000  sleep 10
$ ps -o pid,rgid,egid,sgid,cmd | grep sleep
14766  1000  1000  1000  sleep 10
```

#### 1.2.3. The root account

The name of the root account (aka superuser account) is `root`

`root` has `UID 0`

Any process for which the effective UID is `0` can perform any valid operation on any file or process. Operations that are not valid, such as executing a file on which the execute (`x`) permission bit is not set are forbidden even for `root`

#### 1.2.4. Set-UID execution

Some programs may require to run with privileges that the user who run them does not have. An example is `passwd`, the program that let users change their password

Login passwords are stored in `/etc/shadow`

```shell
ls -l /etc/shadow
-rw-r----- 1 root shadow [...] /etc/shadow
```

- `root` can read and write, but not execute (`rw-`)
- Who is a member of `shadow` can only read (`r--`)
- The others cannot do anything (`---`)

---

```shell
$ ls -l $(which passwd)
-rwsr-xr-x 1 root root [...] /usr/bin/passwd
```

- `root` can read, write, and execute (`rws`)
    - `s` means that `passwd` is a set-UID program, which means that when `passwd` is running, the effective UID is set to `0` (`root`)
- Who is member of `root` can read and execute, but not write (`r-x`)
- The others can read and execute, but not write (`r-x`)  

---

When the kernel runs an executable file with the set-UID (`s`), the kernel changes the effective UID to the owner of the file instead of the UID of the user who actually ran the command

1. When `ubuntu` runs an executable file, that process will usually have real UID, real GID, effective UID, and effective GID that equal `1000` (as `ubuntu` UID and GID are both `1000`)
2. `ubuntu` can run `passwd`. In fact, `ubuntu` is neither `root` nor a member of `root`, but everyone can read and execute `passwd`
3. `passwd` has the set-UID permission bit (`s`). This means that when `passwd` executes as a process, the kernel changes its effective UID to the UID of the owner of the file, i.e., `root`, thus `0`
4. the process `passwd` executed by `ubuntu` can read and write `/etc/shadow`, as it is running with `root` privileges
5. `ubuntu` could change its password without actually having the privileges to neither read nor write `/etc/shadow`

---

Note that although `root` can read and write `/etc/shadow`, it cannot see login passwords anyway, as they are saved as hashes

```shell
$ sudo cat /etc/shadow | grep ubuntu
ubuntu:$y$j9T$RUQLHa1CYOgOURxJYy0DA0$RWGAlTnL0gX6xQEQjDRq61lYGOGeBt6SIDb5DzDOwq7:20151:0:99999:7:::
```

---

| Field    | Meaning                                                                             |
| -------- | ----------------------------------------------------------------------------------- |
| `ubuntu` | Username                                                                            |
| `$...$`  | Hashed password                                                                     |
| `20151`  | Number of days since January 1, 1970, when the password was last changed            |
| `0`      | Days a user must wait before changing the password again (`0` means no restriction) |
| `99999`  | Days after which the password expires (`99999` means the password never expires)    |
| `7`      | Days before expiration that the system warns the user to change the password        |

---

| Field                      | Meaning                      |
| -------------------------- | ---------------------------- |
| `$y$`                      | Yescrypt hashing algorithm   |
| `$j9T$`                    | Parameters for the algorithm |
| `$RUQLHa1CYOgOURxJYy0DA0$` | Salt                         |
| `$RWGAlTnL0 [...]`         | The actual hashed password   |

---

```shell
>>> import crypt
>>> stored_hash = (
... "$y$j9T$RUQLHa1CYOgOURxJYy0DA0$RWGAlTn"
... "L0gX6xQEQjDRq61lYGOGeBt6SIDb5DzDOwq7"
... )
>>> password = "ubuntu"
>>> salt = "$".join(stored_hash.split("$")[:4])
>>> computed_hash = crypt.crypt(password, salt)
>>> computed_hash == stored_hash
True
```

## 2. Rootly powers

### 2.1. Root account login

Most systems let users log in as `root` . This is a bad idea
- Root logins leave no record of what operations were performed as `root`
- If several people can login as `root`, there is no way to say who did what

For these reasons some systems forbid it by default, such as Ubuntu

```shell
$ sudo cat /etc/shadow | grep root
root:*:19882:0:99999:7:::
```

`*` means that password-based login for `root` is disabled

### 2.2. Substituting user identities

The `su` command let users change identity
- Without any argument, `su` prompts for the `root` password and then starts a root shell. Type `exit` or `Ctrl + D` to exit from the root shell

`su` is a better way to become `root` than log in. Although `su` does not record the commands executed as `root`, `su` creates a log entry that states who became `root` and when

---

A good habit is to type the full pathname to `su`, rather than relying on the shell to find it for you. This gives you some protection agains other programs called `su` that might have been sneaked into your search path with the intention of harvesting passwords

```shell
$ which su
/usr/bin/su
```

---

If the command is neither a built-in nor an alias, the shell looks for it in the directories listed in the `PATH` environment variable

```shell
$ echo $PATH
/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin
```

---

For example, when you type `su`, the shell looks for `su` in
1. `/usr/local/sbin/su`
2. `/usr/local/bin/su`
3. `/usr/sbin/su`
4. `/usr/bin/su` $\rightarrow$ found

This means that an executable file called `su` in `/usr/local/sbin` would take precedence over the system default one

### 2.3. Executing commands as another user

The `sudo` command takes as its argument a command line to be executed as `root` (or another restricted user)

1. `sudo` looks into `/etc/sudoers`, which lists the people who are authorized to use `sudo` and the commands they are allowed to run on each host
2. if the command is permitted, `sudo` prompts for the **user's password** 
3. if the password is correct, `sudo` executes the command

#### 2.3.1. Logs

`sudo` logs the commands that were executed

```shell
$ ls -l /etc/shadow
-rw-r----- [...] root shadow [...] /etc/shadow
$ whoami
ubuntu
$ cat /etc/shadow | grep ubuntu
cat: /etc/shadow: Permission denied
$ sudo cat /etc/shadow | grep ubuntu
ubuntu:$y$j9T$ [...]:0:99999:7:::
$ grep sudo /var/log/auth.log | grep cat | tail -n 1
2025-03-05T13:38:03.810850+00:00 admin sudo:   ubuntu : TTY=pts/0 ; PWD=/home/ubuntu ; USER=root ; COMMAND=/usr/bin/cat /etc/shadow
```

---

| Field                              | Meaning                                          |
| ---------------------------------- | ------------------------------------------------ |
| `2025-03-05T13 [...]`              | Timestamp                                        |
| `admin`                            | Host where the command was executed              |
| `sudo`                             | Who is the subject of the log entry              |
| `ubuntu`                           | The user who ran `sudo`                          |
| `TTY=pts/0`                        | Terminal from which the command was executed     |
| `PWD=/home/ubuntu`                 | Directory from which the command was executed    |
| `USER=root`                        | The target user that the command was executed as |
| `COMMAND=/usr/bin/cat /etc/shadow` | Command that was executed by `sudo`              |

#### 2.3.2. The sudoers file

`/etc/sudoers` is designed so that a single version can be used on several hosts at once

```shell
$ sudo cat /etc/sudoers
Host_Alias CS = tigger, anchor, piper, moet, sigi
Host_Alias PHYSICS = eprince, pprince, icarus
 
Cmnd_Alias DUMP = /sbin/dump, /sbin/restore 
Cmnd_Alias WATCHDOG = /usr/local/bin/watchdog
Cmnd_Alias SHELLS = /bin/sh, /bin/dash, /bin/bash

mark, ed PHYSICS = ALL
herb     CS = /usr/bin/tcpdump : PHYSICS = (operator) DUMP
lynda    ALL = (ALL) ALL
%wheel   ALL, !PHYSICS = NOPASSWD: WATCHDOG
```

---

The first group of lines defines host aliases

```
Host_Alias CS = tigger, anchor, piper, moet, sigi
Host_Alias PHYSICS = eprince, pprince, icarus
```

`Host_Alias` defines an alias (e.g., `CS`) for one or more hosts (e.g., `tigger`, `anchor`, `piper`, `moet`, and `sigi`—the hosts of the department of computer science)

---

The second group of lines defines command aliases

```
Cmnd_Alias DUMP = /sbin/dump, /sbin/restore 
Cmnd_Alias WATCHDOG = /usr/local/bin/watchdog 
Cmnd_Alias SHELLS = /bin/sh, /bin/dash, /bin/bash
```

`Cmnd_Alias` defines an alias (e.g., `DUMP`) for one or more commands (e.g., `/sbin/dump` and `/sbin/restore`)

---

The third group of lines defines permissions

```
mark, ed PHYSICS = ALL
herb     CS = /usr/bin/tcpdump : PHYSICS = (operator) DUMP
lynda    ALL = (ALL) ALL, !SHELLS
%wheel   ALL, !PHYSICS = NOPASSWD: WATCHDOG
```

Each permission line includes information about:
- The users to whom the line applies
- The hosts on which the line applies
- The users as whom the commands can be executed (target users)
- The commands that the users can run

---

| User            | Host                   | Target user                      | Command               |
| --------------- | ---------------------- | -------------------------------- | --------------------- |
| `mark` and `ed` | `PHYSICS`              | `root`                           | `ALL`                 |
| `herb`          | `CS`                   | `root`                           | `/usr/bin/tcpdump`    |
|                 | `PHYSICS`              | `operator`                       | `DUMP`                |
| `lynda`         | `ALL`                  | `ALL`                            | `ALL` except `SHELLS` |
| `%wheel`        | `ALL` except `PHYSICS` | `root` with no password required | `WATCHDOG`            |

- Users to whom the line applies are listed between parenthesis
    - If none is provided, the line applies to `root`
- `%` is to specify a group rather than a user

---

The "allow all commands except..." type of permission is doomed to fail

An easy way to circumvent the permission that allows `lynda` to run any command except `SHELLS` as any user on any host is the following

```shell
$ cp /bin/sh /tmp/sh
$ sudo /tmp/sh
```

#### 2.3.3. Permission precedence

A given invocation of `sudo` might potentially be addressed by several entries in `/etc/sudoers`

The rule is that `sudo` always applies the **last** matching line, where matching being determined by the entire 4-tuple of user, host, target user, and command

---

Suppose the following `/etc/sudoers` file and `alice` belongs to the `wheel` group

```
User_Alias   ADMINS = alice, bob, charles
User_Alias   MYSQL_ADMINS = alice, bob

%wheel       ALL = (ALL) ALL
MYSQL_ADMINS ALL = (mysql) NOPASSWD: ALL
ADMINS       ALL = (ALL) NOPASSWD: /sbin/dump
```

`alice` must only enter their password for any command that is not explicitly covered by a `NOPASSWD` permission line

---

Suppose the permission lines are reversed

```
User_Alias   ADMINS = alice, bob, charles
User_Alias   MYSQL_ADMINS = alice, bob

ADMINS       ALL = (ALL) NOPASSWD: /sbin/dump
MYSQL_ADMINS ALL = (mysql) NOPASSWD: ALL
%wheel       ALL = (ALL) ALL
```

`alice` must always enter their password

#### 2.3.4. Editing permissions

Always edit `/etc/sudoers` with the `visudo` command, which
- Opens the file with a text editor of your choice
- Validates the syntax of the file upon saving, this preventing configuration errors

```shell
$ sudo update-alternatives --config editor
There are 4 choices for the alternative editor (providing /usr/bin/editor).

Selection  Path               Priority   Status
-------------------------------------------------
0          /bin/nano          40        auto mode
1          /bin/ed            -100      manual mode
2          /bin/nano          40        manual mode
* 3        /usr/bin/vim.basic 30        manual mode
4          /usr/bin/vim.tiny  15        manual mode

Press <enter> to keep the current choice[*], or type selection number:
```

---

On Ubuntu, `/etc/sudoers` looks like the following (comments removed)

```shell
Defaults        env_reset
Defaults        mail_badpass
Defaults        secure_path="/usr/local/sbin: [...]"

root    ALL=(ALL:ALL) ALL
%admin  ALL=(ALL) ALL
%sudo   ALL=(ALL:ALL) ALL

@includedir /etc/sudoers.d
```

- `env_reset` removes user's environment variables (safety measure)
- `mail_badpass` mails notices of bad `sudo` password attempts
- `secure_path` specifies the `PATH` value that will be used for `sudo`
- `@includedir` indicates that files within `/etc/sudoers.d` will be appended to the `sudo` configuration

---

Always edit files in `/etc/sudoers.d` with `visudo`
- `sudo visudo -f /etc/sudoers.d/<file-to-edit>`

Files in `/etc/sudoers.d`
- Are appended to the `sudo` configuration in lexicographical order
- Follow the same rules as `/etc/sudoers`

---

By default, `sudo` saves authentication details for a certain amount of time. This means that a user is not required to type their password again until that timer runs out

To clear the timer

```shell
$ sudo -k
```

To prime or renew the lease

```shell
$ sudo -v
[sudo] password for ubuntu:
```

---

The easiest way to get to know which permissions apply to your user is

```shell
$ sudo -l
Matching Defaults entries for ubuntu on admin:
    env_reset, mail_badpass, secure_path=/usr/local/sbin [...]

User ubuntu may run the following commands on admin:
    (ALL : ALL) ALL
    (ALL) NOPASSWD: ALL
```

### 2.4. Final remarks

#### 2.4.1. Pros and cons of sudo

| Pro                                                                                          | Con                                                                                             |
| -------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| Command logging                                                                              | Command logging can be easily subverted (`sudo su`, although `sudo su`would at least be logged) |
| Users can do stuff that requires root privileges without having unlimited root privileges    |                                                                                                 |
| Users do not have to know the `root` password because `sudo` prompts for the user's password | Any breach in the security of a sudoer's personal account can be equivalent to breaching `root` |
| Faster of both `su` and `root` login                                                         |                                                                                                 |
| Privileges can be revoked without changing the `root`password                                |                                                                                                 |
| A list of all users with `root` privileges is maintained                                     |                                                                                                 |
| Lower chance of a `root` shell left unattended                                               |                                                                                                 |
| A single file can control access for an entire network                                       |                                                                                                 |

#### 2.4.2. Best practices

As a rule of thumb
- Forbid `root` login
- Make `sudo` the primary way to become `root`
- Reserve `su` for emergencies, such as misconfiguration of `sudo`

About `sudo`
- Always use `visudo` to edit `sudo` configuration
- Technically speaking, any attempt to "allow all commands except..." is doomed to fail
- Avoid `NOPASSWD`, if you can. If you must, restrict passwordless execution as much as possible

## Glossary

| Term                      | Meaning                                                                                                                                                                                            |
| ------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Access control            | How the kernel and its delegates make security-related decisions                                                                                                                                   |
| Access control model      | A model that determines who can access what and how                                                                                                                                                |
| Group                     | A collection of users with shared permissions                                                                                                                                                      |
| Group identifier (GID)    | A value that identifies a group                                                                                                                                                                    |
| Network file system (NFS) | A distributed filesystem protocol originally developed by Sun Microsystems in 1984                                                                                                                 |
| Object                    | A resource that access control applies to                                                                                                                                                          |
| Owner                     | The user who owns the object. Typically, the owner is the user who created the object                                                                                                              |
| `PATH`                    | An environment variable that lists directories where executable files are located. When a user prompts a command, the shell searches these directories to locate the corresponding executable file |
| Permission bits           | Nine bits that define who can access a file or directory and what actions they can perform                                                                                                         |
| Process scheduling        | A mechanism of the OS that decides which process runs at a certain point in time                                                                                                                   |
| Process signal            | A notification sent to a process that some condition has occurred                                                                                                                                  |
| `root` (aka superuser)    | A special account that can act as the owner of any object                                                                                                                                          |
| Salt                      | A random value provided as an additional input to a one-way function before hashing                                                                                                                |
| Security                  | How to set up a system or network to minimize the chance of unwelcome access by intruders                                                                                                          |
| The sudoers file          | A file whose path is `/etc/sudoers` that contains the `sudo` configuration                                                                                                                         |
| UNIX                      | A family of OSes that derive from the original AT&T Unix, whose development started in 1969 at Bell Labs by Thompson, K. et al.                                                                    |
| User                      | An individual account with assigned permissions                                                                                                                                                    |
| User identifier (UID)     | A value that identifies a user                                                                                                                                                                     |

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
