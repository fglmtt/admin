# User management

## Table of contents

- [1. Users](#1-users)
- [2. Anatomy of a user account](#2-anatomy-of-a-user-account)
    - [2.1. The passwd entry](#21-the-passwd-entry)
    - [2.2. The shadow entry](#22-the-shadow-entry)
    - [2.3. The home directory and startup files](#23-the-home-directory-and-startup-files)
    - [2.4. Ownerships](#24-ownerships)
- [3. Commands for managing users](#3-commands-for-managing-users)
    - [3.1. Defaults](#31-defaults)
    - [3.2. Adding users](#32-adding-users)
    - [3.3. Setting up initial passwords](#33-setting-up-initial-passwords)
    - [3.4. Locking and unlocking passwords](#34-locking-and-unlocking-passwords)
    - [3.5. Removing users](#35-removing-users)
- [4. Commands for managing groups](#4-commands-for-managing-groups)
    - [4.1. Adding groups](#41-adding-groups)
    - [4.2. Adding users to a group](#42-adding-users-to-a-group)
    - [4.3. Removing groups](#43-removing-groups)
- [Glossary](#glossary)
- [Bibliography](#bibliography)
- [Licenses](#licenses)

## 1. Users

A user is really nothing more than a number: an unsigned 32-bit integer known as user identifier (UID). Almost everything related to user management revolves around this number.

> [!warning]
> Account hygiene is a key determinant of system security. Prime targets for attackers are:
> 
> - Infrequently used accounts
> - Accounts with easily guessed passwords

## 2. Anatomy of a user account

### 2.1. The passwd entry

The account record lives in [`/etc/passwd`](https://github.com/fglmtt/admin/blob/main/lectures/access-control-and-rootly-powers.md#121-filesystem-access-control). It binds a username to a UID, a primary GID, a home directory, and a login shell.

Manual maintenance of `/etc/passwd` is error prone and inefficient.

> [!tip]
> If you do have to make manual changes, use the `vipw` command. `vipw` locks `/etc/passwd` so that editing sessions cannot collide. `vipw -s` does the same for `/etc/shadow`.

### 2.2. The shadow entry

The hashed password and password-aging metadata live in [`/etc/shadow`](https://github.com/fglmtt/admin/blob/main/lectures/access-control-and-rootly-powers.md#124-set-uid-execution), readable only by `root`.

A fresh account has no usable password until one is set. Until then, the hash field holds a placeholder (`!` or `*`) that blocks password authentication.

> [!warning]
> Some automated systems for adding new users do not require you to set an initial password; they force the user to set a password on first login. Although this feature is convenient, it's a security hole: anyone who can guess new login names can hijack accounts before the intended users have had a chance to log in.

### 2.3. The home directory and startup files

Every account has a home directory, recorded in the sixth field of its `/etc/passwd` entry. There is nothing magical about it — it is an ordinary directory that the shell `cd`s into at login.

A startup file is a script that the shell runs automatically when it starts, so that each user gets a customized environment without having to set it up by hand. Startup files traditionally begin with a dot and end with the letters `rc`, short for "run command". For example, `bash` reads `~/.bashrc` whenever the user opens a new terminal.

New accounts are typically seeded with a default set of startup files copied from `/etc/skel`.

### 2.4. Ownerships

The home directory and its startup files must be owned by the new user, otherwise the user cannot read or modify them

```bash
$ sudo chown -R <new-user>:<new-group> ~<new-user>
```

- `-R` applies the change recursively
- `~<new-user>` is a shorthand for `/home/<new-user>`

## 3. Commands for managing users

### 3.1. Defaults

Most Linux distributions include a basic `useradd` suite that draws its configuration parameters from `/etc/login.defs` and `/etc/default/useradd`. The `login.defs` file is maintained by hand. Parameters in the `useradd` file, instead, are set through the `useradd` command itself.

Typical defaults are to put new users in individual groups, to hash passwords with a strong algorithm (e.g., yescrypt), and to populate new users' home directories with startup files from `/etc/skel`.

On Linux, UIDs below 1000 are reserved for system accounts (e.g., daemons) and UIDs from 1000 upward are assigned to regular users.

---

To see the defaults

```bash
$ useradd -D
```

To update a default value

```bash
$ sudo useradd -D -s /bin/bash
```

sets `/bin/bash` as the default shell.

### 3.2. Adding users

The basic form of the `useradd` command accepts the name of the new account on the command line

```bash
$ sudo useradd -m hilbert
```

This command creates `hilbert`'s home directory, an entry in `/etc/passwd`, and a corresponding entry in `/etc/shadow`

```bash
$ grep hilbert /etc/passwd
hilbert:x:1001:1001::/home/hilbert:/bin/bash
```

---

`useradd` disables the new account by default by putting `!` in the password field of `/etc/shadow`

```bash
$ sudo grep hilbert /etc/shadow
hilbert:!:20552:0:99999:7:::
```

> [!tip]
> Both `!` and `*` block password authentication. On Ubuntu, the convention is
> 
> - `!`: human account, not yet usable or temporarily locked
> - `*`: system account, by design no password (e.g., `root`)

### 3.3. Setting up initial passwords

Unlock the account by setting a password

```bash
$ sudo passwd hilbert
New password:
Retype new password:
passwd: password updated successfully
```

The `!` placeholder in `/etc/shadow` is replaced by the hashed password

```bash
$ sudo grep hilbert /etc/shadow
hilbert:$y$j9T$AQBiUDKEJ806Jx740GP6f.$2zmDBt/LupCvcQt5BlHTG8CWsIwe30aZFA5XWj4xp5D:20552:0:99999:7:::
```

---

Test the account by switching to `hilbert` with `su`

```bash
$ su -l hilbert
Password:
$ pwd
/home/hilbert
$ whoami
hilbert
```

- `-l` starts a login shell and moves into `hilbert`'s home directory, as if `hilbert` had just logged in

To leave `hilbert`'s identity and return to your original shell, type `exit` or press `Ctrl + D`.

---

Force `hilbert` to change the password on first login

```bash
$ sudo chage -d 0 hilbert
```

- `-d 0` sets the last-change field to `0`, a sentinel value that the system treats as "the administrator has forced a password change on next login", regardless of the expiration field

On the next login, `hilbert` will be prompted to pick a new password before reaching the shell.

---

Switching to `hilbert` now triggers the forced password change

```bash
$ su -l hilbert
Password:
You are required to change your password immediately (administrator enforced).
Changing password for hilbert.
Current password:
```

`hilbert` must supply the current password once more (to prove identity) and then pick a new one before the shell starts.

### 3.4. Locking and unlocking passwords

On occasion, a user's login must be temporarily disabled.

A straightforward way to do this is to put a `!` in front of the user's hashed password in the `/etc/shadow` file.

The `usermod` command provides options to easily lock (`-L`) and unlock (`-U`) passwords, which are just shortcuts for the password twiddling described above.

---

```bash
$ sudo usermod -L hilbert
$ sudo grep hilbert /etc/shadow
hilbert:!$y$j9T$AQBiUDKEJ806Jx740GP6f.$2zmDBt/LupCvcQt5BlHTG8CWsIwe30aZFA5XWj4xp5D:20552:0:99999:7:::
```

> [!warning]
> Locking the password this way simply makes logins fail. It does not notify the user of the account suspension or explain why the account no longer works. In addition, commands that do not necessarily check the password (e.g., `ssh`) may continue to function.

### 3.5. Removing users

When a user leaves your organization, that user's login account and files must be removed from the system. If possible, don't do that chore by hand; let `userdel` handle it

```bash
$ sudo userdel -r hilbert
$ grep hilbert /etc/passwd
$ ls -l /home/hilbert
ls: cannot access '/home/hilbert': No such file or directory
```

> [!tip]
> Before you remove someone's home directory, be sure to relocate any files that are needed by other users. You can't be sure which files those might be, so it's always a good idea to make a backup of the user's home directory before deleting it.

---

Once you have removed all traces of a user, you may want to verify that the user's old UID no longer owns files on the system

```bash
$ sudo find <filesystem> -xdev -nouser
```

- `<filesystem>` is the starting point of the search
- `-xdev` makes sure `find` does not cross filesystem boundaries
- `-nouser` matches files whose UID does not correspond to any entry in `/etc/passwd`

## 4. Commands for managing groups

Group management follows the same pattern as user management.

The `groupadd`, `groupmod`, and `groupdel` commands are the group counterparts of `useradd`, `usermod`, and `userdel`, respectively.

> [!warning]
> Group membership is traditionally changed with `usermod`, since it is a user's property. Recent versions of `groupmod` also support adding users. However, `usermod` remains the more portable option.

### 4.1. Adding groups

The basic form of the `groupadd` command accepts the name of the new group on the command line

```bash
$ sudo groupadd faculty
$ grep faculty /etc/group
faculty:x:1002:
$ sudo grep faculty /etc/gshadow
faculty:!::
```

> [!note]
> The `!` in `/etc/gshadow` means that no password is set for the group. Group passwords are rarely used in practice, so this field is almost always `!` or `*`.

### 4.2. Adding users to a group

Add an existing user to a group with `usermod`

```bash
$ sudo usermod -aG faculty hilbert
$ grep faculty /etc/group
faculty:x:1002:hilbert
```

- `-G` specifies supplementary groups
- `-a` (append) is essential: without it, `usermod -G` overwrites `hilbert`'s supplementary groups with just `faculty`, silently dropping the others

---

```bash
$ grep faculty /etc/group
faculty:x:1002:hilbert
$ id
uid=1001(hilbert) gid=1001(hilbert) groups=1001(hilbert)
```

> [!note]
> There is no `faculty` in the `id` output because `hilbert`'s shell inherited the groups at login. The new membership takes effect on `hilbert`'s next login.

### 4.3. Removing groups

Remove a group with `groupdel`

```bash
$ sudo groupdel faculty
$ grep faculty /etc/group
```

> [!warning]
> `groupdel` refuses to remove a group that is the primary group of any user. Reassign those users' primary group with `usermod -g` before deleting.

---

Once you have removed the group, you may want to verify that the old GID no longer owns files on the system

```bash
$ sudo find <filesystem> -xdev -nogroup
```

- `-nogroup` matches files whose GID does not correspond to any entry in `/etc/group`

## Glossary

| Term                                        | Meaning                                                                                                                                        |
| ------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| `/etc/group`                                | The file that lists groups and their members                                                                                                   |
| `/etc/gshadow`                              | The file that stores group passwords, administrators, and members                                                                             |
| `/etc/passwd`                               | The file that lists user accounts on the system                                                                                                |
| `/etc/shadow`                               | The file that stores users' hashed passwords and password-aging metadata                                                                       |
| `/etc/skel`                                 | The template directory whose contents are copied into each new user's home directory                                                           |
| `chage`                                     | A command that changes user password-aging metadata in `/etc/shadow`                                                                           |
| Group                                       | A collection of users with shared permissions                                                                                                  |
| `groupadd`                                  | A command that creates a new group                                                                                                             |
| `groupdel`                                  | A command that removes a group                                                                                                                 |
| `groupmod`                                  | A command that modifies an existing group                                                                                                      |
| Group identifier (GID)                      | A value that identifies a group                                                                                                                |
| Hash (aka digest, checksum, or fingerprint) | The output value of a hash function                                                                                                            |
| Home directory                              | The directory a user lands in at login, where startup files and personal data are stored                                                       |
| Login shell                                 | The shell that runs as a user's first process at login; recorded in the seventh field of `/etc/passwd`                                         |
| `passwd`                                    | A command that sets or changes a user's password                                                                                               |
| Primary group                               | The group recorded in the fourth field of a user's `/etc/passwd` entry; assigned to files the user creates by default                          |
| `root` (aka superuser)                      | A special account that can act as the owner of any object                                                                                      |
| Startup file                                | A script that the shell runs automatically when it starts, so that each user gets a customized environment without having to set it up by hand |
| `su`                                        | A command that lets users change identity                                                                                                      |
| `sudo`                                      | A command that executes a command as another user, typically `root`                                                                            |
| Supplementary group                         | Any additional group a user belongs to beyond their primary group; recorded in `/etc/group`                                                    |
| System account                              | An account for a daemon or service, conventionally assigned a UID below 1000                                                                   |
| User                                        | An individual account with assigned permissions                                                                                                |
| `useradd`                                   | A command that creates a new user account                                                                                                      |
| `userdel`                                   | A command that removes a user account                                                                                                          |
| User identifier (UID)                       | A value that identifies a user                                                                                                                 |
| `usermod`                                   | A command that modifies an existing user account                                                                                               |

## Bibliography

| Author(s)         | Title                                                                   | Year |
| ----------------- | ----------------------------------------------------------------------- | ---- |
| Nemeth, E. et al. | [UNIX and Linux System Administration Handbook](https://www.admin.com/) | 2018 |
| Community         | [Wikipedia](https://en.wikipedia.org/)                                  | 2025 |

## Licenses

| Content | License |
| ------- | ------- |
| Code    | [MIT License](https://mit-license.org/) |
| Text    | [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International](https://creativecommons.org/licenses/by-nc-sa/4.0/) |
