# September 16, 2026

## Italian

Durata esame: 2 ore e 30 minuti.

| Sezione                            | Punti |
| ---------------------------------- | ----- |
| Processo periodico (§1)            | 16    |
| - Script Python (§1.1)             | 8/16  |
| - Service (§1.2)                   | 4/16  |
| - Timer (§1.3)                     | 4/16  |
| Amministrazione degli account (§2) | 8     |
| Domande a risposta aperta (§3)     | 9     |

### 1. Processo periodico

#### 1.1. Script Python

Scrivi uno script Python che ordina per estensione i file presenti in una directory specificata e in tutte le sue sottodirectory, spostando ogni file la cui estensione è tra quelle da monitorare in una sottodirectory di una directory di destinazione chiamata come tale estensione, e registrando ogni spostamento in un file di log. Nella tua home directory, crea una directory chiamata `extension-sorter` e, al suo interno, un file chiamato `app.py`, utilizzando questo template:

```python
# nome e cognome:
# matricola:
#
# path:

import argparse
from datetime import datetime
import os
import shutil
import sys

def main():
    pass


if __name__ == "__main__":
    main()
```

Lo script deve accettare esattamente quattro argomenti da linea di comando, analizzati con il modulo `argparse`. Il primo argomento, `--path`, è una stringa obbligatoria che indica il percorso assoluto della directory da scansionare. Il secondo argomento, `--dest`, è una stringa obbligatoria che indica il percorso assoluto della directory di destinazione all'interno della quale sono create le sottodirectory per estensione. Il terzo argomento, `--extensions`, è una stringa obbligatoria che elenca le estensioni da monitorare, separate da virgole e scritte senza il punto iniziale. Il quarto argomento, `--log`, è una stringa obbligatoria che indica il percorso assoluto del file di log su cui scrivere.

Dopo il parsing, valida gli input: verifica che `--path` sia assoluto (`os.path.isabs`), esista (`os.path.exists`) e sia una directory (`os.path.isdir`); verifica che `--dest` sia assoluto (`os.path.isabs`), esista (`os.path.exists`) e sia una directory (`os.path.isdir`); suddividi `--extensions` sulle virgole (`str.split`) e verifica che nessuna delle estensioni ottenute sia una stringa vuota; verifica che `--log` sia un percorso assoluto (`os.path.isabs`). Se uno dei controlli fallisce, stampa un messaggio di errore esplicativo sullo standard error (`print`) ed esci con un codice di stato diverso da zero (`sys.exit`).

Una volta validati, assicurati che la directory che conterrà il file di log esista (`os.path.dirname`, `os.makedirs`) e crea all'interno di `--dest` una sottodirectory per ogni estensione (`os.path.join`, `os.makedirs`). Quindi percorri ricorsivamente l'albero delle directory al percorso fornito come primo argomento (`os.listdir`, `os.path.join`, `os.path.isdir`). Per ogni file incontrato (`os.path.isfile`), verifica se il suo nome termina con una delle estensioni (`str.endswith`). In caso affermativo, sposta il file nella sottodirectory chiamata come tale estensione (`shutil.move`), quindi apri in modalità append il file di log indicato da `--log` (`open`) e scrivi una riga contenente la data e l'ora correnti (`datetime.now`), il percorso originale del file e la directory in cui è stato spostato. I file la cui estensione non è tra quelle da monitorare restano dove sono. Assumi che `--dest` non sia all'interno di `--path` e che non esistano due file con lo stesso nome nell'albero, così che uno spostamento non sovrascriva mai un file esistente.

Ad esempio, eseguendo

```shell
$ python ~/extension-sorter/app.py \
    --path ~/inbox \
    --dest ~/sorted \
    --extensions pdf,txt \
    --log ~/extension-sorter.log
```

lo script esaminerà `~/inbox` e tutte le sue sottodirectory, spostando ogni file il cui nome termina con `.pdf` in `~/sorted/pdf` e ogni file il cui nome termina con `.txt` in `~/sorted/txt`, e registrando ogni spostamento in `~/extension-sorter.log`. I file con qualsiasi altra estensione, così come i file senza estensione, restano dove sono.

#### 1.2. Service

Crea un'unità service chiamata `extension-sorter.service` nella tua istanza utente di `systemd`. Configurala per avviare `~/extension-sorter/app.py` con gli argomenti `--path %h/inbox`, `--dest %h/sorted`, `--extensions pdf,txt` e `--log %h/extension-sorter.log`. Usa questo template:

```
# nome e cognome:
# matricola:
#
# path:
```

#### 1.3. Timer

Crea un'unità timer chiamata `extension-sorter.timer` nella tua istanza utente di `systemd`. Configurala per attivare `extension-sorter.service` alle 05:30 di ogni mercoledì e sabato. Usa questo template:

```
# nome e cognome:
# matricola:
#
# path:
#
# comando per abilitare il timer:
# comando per avviare il timer:
```

### 2. Amministrazione degli account

Configura `sudo` su una rete di cinque host Linux: `web01`, `web02`, `web03`, `db01` e `db02`. La rete ha i seguenti utenti e gruppi:

| Utente  | Gruppo primario | Gruppi aggiuntivi |
| ------- | --------------- | ----------------- |
| `alma`  | `alma`          |                   |
| `bruno` | `bruno`         |                   |
| `cleo`  | `cleo`          | `acct`            |
| `dario` | `dario`         | `net`             |
| `elin`  | `elin`          | `pkg`             |

Applica le seguenti regole:

| Categoria | Regola                                                                                                                                                                                |
| --------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Alias     | Definisci `Host_Alias WEB = web01, web02, web03` e `Host_Alias DB = db01, db02`                                                                                                      |
| Alias     | Definisci `Cmnd_Alias FWTOOLS = /usr/sbin/iptables, /usr/bin/tcpdump`, `Cmnd_Alias ACCTMGM = /usr/sbin/useradd, /usr/sbin/usermod` e `Cmnd_Alias PKGMGM = /usr/bin/apt, /usr/bin/dpkg` |
| Permessi  | `alma` può eseguire qualsiasi comando come qualsiasi utente su qualsiasi host                                                                                                        |
| Permessi  | `bruno` può eseguire qualsiasi comando come qualsiasi utente su qualsiasi host, eccetto `FWTOOLS`                                                                                    |
| Permessi  | `%acct` può eseguire `ACCTMGM` come `root` su `WEB`                                                                                                                                  |
| Permessi  | `%pkg` può eseguire `PKGMGM` come `root` su `DB`, senza password                                                                                                                     |
| Permessi  | `cleo` può eseguire `/usr/bin/cat /etc/gshadow` come `root` su qualsiasi host, senza password                                                                                        |
| Permessi  | `dario` può eseguire `/usr/bin/id` come `elin` su `db01`                                                                                                                             |
| Permessi  | `%net, %pkg` può eseguire `/usr/sbin/ip` come `root` su qualsiasi host, senza password                                                                                               |

Il file deve essere creato in `/etc/sudoers.d/site`. Usa questo template:

```
# nome e cognome:
# matricola:
#
# path:
```

### 3. Domande a risposta aperta

1. Quali sono gli scopi dei bit set-UID, set-GID e sticky, a quali file regolari o directory si applica ciascuno di essi e in che modo alterano i controlli sui permessi?
2. Come può un amministratore bloccare e sbloccare l'account di un utente, come funziona il meccanismo sottostante a livello di `/etc/shadow` e quali sono i limiti di questo approccio?
3. Che cos'è il social engineering, perché è particolarmente difficile difendersene e qual è una forma comune di questo attacco?

Usa questo template:

```
# nome e cognome:
# matricola:

1.

2.

3.
```

## English

Exam duration: 2 hours and 30 minutes.

| Section                     | Points |
| --------------------------- | ------ |
| Periodic process (§1)       | 16     |
| - Python script (§1.1)      | 8/16   |
| - Service (§1.2)            | 4/16   |
| - Timer (§1.3)              | 4/16   |
| Account administration (§2) | 8      |
| Open-ended questions (§3)   | 9      |

### 1. Periodic process

#### 1.1. Python script

Write a Python script that sorts the files in a specified directory and all its subdirectories by extension, moving each file whose extension is among those to monitor into a subdirectory of a destination directory named after that extension, and recording every move in a log file. In your home directory, create a directory called `extension-sorter` and, inside it, a file called `app.py`, using this template:

```python
# first and last name:
# student id:
#
# path:

import argparse
from datetime import datetime
import os
import shutil
import sys

def main():
    pass


if __name__ == "__main__":
    main()
```

The script must accept exactly four command-line arguments, parsed with the `argparse` module. The first argument, `--path`, is a required string indicating the absolute path of the directory to scan. The second argument, `--dest`, is a required string indicating the absolute path of the destination directory under which the per-extension subdirectories are created. The third argument, `--extensions`, is a required string listing the extensions to monitor, separated by commas and written without a leading dot. The fourth argument, `--log`, is a required string indicating the absolute path of the log file to write to.

After parsing, validate the inputs: check that `--path` is absolute (`os.path.isabs`), exists (`os.path.exists`), and is a directory (`os.path.isdir`); check that `--dest` is absolute (`os.path.isabs`), exists (`os.path.exists`), and is a directory (`os.path.isdir`); split `--extensions` on commas (`str.split`) and verify that none of the resulting extensions is an empty string; check that `--log` is an absolute path (`os.path.isabs`). If any check fails, print an explanatory error message to standard error (`print`) and exit with a non-zero status code (`sys.exit`).

Once validated, ensure that the directory that will contain the log file exists (`os.path.dirname`, `os.makedirs`) and create inside `--dest` one subdirectory per extension (`os.path.join`, `os.makedirs`). Then recursively traverse the directory tree at the path provided as the first argument (`os.listdir`, `os.path.join`, `os.path.isdir`). For each file encountered (`os.path.isfile`), check whether its name ends with one of the extensions (`str.endswith`). If it does, move the file into the subdirectory named after that extension (`shutil.move`), then open in append mode the log file indicated by `--log` (`open`) and write a line containing the current date and time (`datetime.now`), the original path of the file, and the directory it was moved into. Files whose extension is not among those to monitor are left where they are. Assume that `--dest` is not inside `--path`, and that no two files in the tree share the same name, so a move never overwrites an existing file.

For example, running

```shell
$ python ~/extension-sorter/app.py \
    --path ~/inbox \
    --dest ~/sorted \
    --extensions pdf,txt \
    --log ~/extension-sorter.log
```

the script will scan `~/inbox` and all its subdirectories, moving every file whose name ends with `.pdf` into `~/sorted/pdf` and every file whose name ends with `.txt` into `~/sorted/txt`, and recording each move in `~/extension-sorter.log`. Files with any other extension, as well as files without an extension, are left where they are.

#### 1.2. Service

Create a service unit named `extension-sorter.service` in your user instance of `systemd`. Configure it to start `~/extension-sorter/app.py` with the arguments `--path %h/inbox`, `--dest %h/sorted`, `--extensions pdf,txt`, and `--log %h/extension-sorter.log`. Use this template:

```
# first and last name:
# student id:
#
# path:
```

#### 1.3. Timer

Create a timer unit named `extension-sorter.timer` in your user instance of `systemd`. Configure it to trigger `extension-sorter.service` at 05:30 on every Wednesday and Saturday. Use this template:

```
# first and last name:
# student id:
#
# path:
#
# command to enable the timer:
# command to start the timer:
```

### 2. Account administration

Configure `sudo` on a fleet of five Linux hosts: `web01`, `web02`, `web03`, `db01`, and `db02`. The fleet has the following users and groups:

| User    | Primary group | Additional groups |
| ------- | ------------- | ----------------- |
| `alma`  | `alma`        |                   |
| `bruno` | `bruno`       |                   |
| `cleo`  | `cleo`        | `acct`            |
| `dario` | `dario`       | `net`             |
| `elin`  | `elin`        | `pkg`             |

Apply the following rules:

| Category    | Rule                                                                                                                                                                                    |
| ----------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Aliases     | Define `Host_Alias WEB = web01, web02, web03` and `Host_Alias DB = db01, db02`                                                                                                           |
| Aliases     | Define `Cmnd_Alias FWTOOLS = /usr/sbin/iptables, /usr/bin/tcpdump`, `Cmnd_Alias ACCTMGM = /usr/sbin/useradd, /usr/sbin/usermod`, and `Cmnd_Alias PKGMGM = /usr/bin/apt, /usr/bin/dpkg`   |
| Permissions | `alma` can run any command as any user on any host                                                                                                                                      |
| Permissions | `bruno` can run any command as any user on any host, except `FWTOOLS`                                                                                                                   |
| Permissions | `%acct` can run `ACCTMGM` as `root` on `WEB`                                                                                                                                            |
| Permissions | `%pkg` can run `PKGMGM` as `root` on `DB`, without a password                                                                                                                           |
| Permissions | `cleo` can run `/usr/bin/cat /etc/gshadow` as `root` on any host, without a password                                                                                                    |
| Permissions | `dario` can run `/usr/bin/id` as `elin` on `db01`                                                                                                                                       |
| Permissions | `%net, %pkg` can run `/usr/sbin/ip` as `root` on any host, without a password                                                                                                           |

The file must be created at `/etc/sudoers.d/site`. Use this template:

```
# first and last name:
# student id:
#
# path:
```

### 3. Open-ended questions

1. What are the purposes of the set-UID, set-GID, and sticky bits, to which regular files or directories does each apply, and how do they alter permission checks?
2. How can an administrator lock and unlock a user's account, how does the underlying mechanism work at the level of `/etc/shadow`, and what are the limitations of this approach?
3. What is social engineering, why is it particularly difficult to defend against, and what is one common form of this attack?

Use this template:

```
# first and last name:
# student id:

1.

2.

3.
```

## Solutions

- [Periodic process (§1)](https://github.com/fglmtt/admin/tree/main/exams/2026-09-16/extension-sorter)
- [Account administration (§2)](https://github.com/fglmtt/admin/blob/main/exams/2026-09-16/sudo)
