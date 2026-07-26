# June 8, 2026 - Session 2

## Italian

Durata esame: 2 ore e 30 minuti.

| Sezione                            | Punti |
| ---------------------------------- | ----- |
| Demone (§1)                        | 16    |
| - Script Python (§1.1)             | 10/16 |
| - Service (§1.2)                   | 6/16  |
| Amministrazione degli account (§2) | 8     |
| Domande a risposta aperta (§3)     | 9     |

Per stampare:

```shell
$ stampa <path/file/da/stampare>
```

> [!warning]
> 1. Scrivere **nome**, **cognome** e numero di matricola su ogni file che si stampa.
> 2. Una volta mandati in stampa i file, avvisare il docente e **rimanere seduti al posto**.

> [!tip]
> 3. Se si nota un errore sul file stampato, lo si può correggere a penna.

### 1. Demone

#### 1.1. Script Python

Scrivi uno script Python che periodicamente analizza una directory specificata (incluse tutte le sue sottodirectory) per rimuovere i file il cui nome inizia con un determinato prefisso. Nella tua home directory, crea la directory `prefix-cleaner` e, al suo interno, il file `app.py`, utilizzando questo template:

```python
# nome e cognome:
# matricola:
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

Lo script deve accettare esattamente quattro argomenti obbligatori da linea di comando, analizzati con il modulo `argparse`: `--target`, che indica il percorso assoluto della directory da ripulire; `--prefix`, che specifica il prefisso del nome dei file da rimuovere; `--interval`, che definisce l'intervallo in secondi (intero positivo) tra ogni controllo; e `--log`, che indica il percorso (assoluto o relativo) della directory dove salvare il file di log. Il nome del file di log è sempre `prefix-cleaner.log`.

Dopo il parsing, valida gli input ricevuti: verifica che il percorso specificato con `--target` sia assoluto (`os.path.isabs`), che esista (`os.path.exists`) e che sia una directory (`os.path.isdir`); controlla che il valore fornito per `--prefix` non sia vuoto; controlla che il valore fornito per `--interval` sia un intero positivo; verifica che il percorso indicato con `--log` esista (`os.path.exists`) e sia una directory (`os.path.isdir`). Se un controllo fallisce, stampa un messaggio di errore esplicativo sullo standard error (`print`) ed esci con un codice di stato diverso da zero (`sys.exit`).

Dopo la validazione, percorri ricorsivamente l'albero delle directory al percorso fornito con `--target` (`os.listdir`, `os.path.join`, `os.path.isdir`). Per ogni file incontrato (`os.path.isfile`), se il suo nome inizia con il prefisso indicato da `--prefix` (`str.startswith`), apri in modalità append il file di log `prefix-cleaner.log` nella directory specificata con `--log` (`open`), scrivi una riga contenente data e ora corrente (`datetime.now`), uno spazio e il percorso assoluto del file, quindi rimuovi il file (`os.remove`). Lo script deve ripetere questa procedura periodicamente, attendendo un numero di secondi pari al valore indicato da `--interval` tra ciascun controllo (`time.sleep`).

Ad esempio, eseguendo:

```shell
$ python ~/prefix-cleaner/app.py \
    --target ~/scratch \
    --prefix tmp \
    --interval 60 \
    --log ~
```

lo script individuerà tutti i file il cui nome inizia con `tmp` presenti in `~/scratch` (e in tutte le sue sottodirectory), scriverà in append in `~/prefix-cleaner.log` la data, l'ora e il percorso di ciascun file, e rimuoverà tali file. Lo script ripeterà l'operazione ogni `60` secondi.

#### 1.2. Service

Crea un'unità service denominata `prefix-cleaner.service` nella tua istanza utente di `systemd`. L'unità deve avviare `~/prefix-cleaner/app.py` con gli argomenti `--target %h/scratch`, `--prefix tmp`, `--interval 60`, e `--log %h`, partire all'avvio del sistema e ripartire in caso di fallimenti. Usa questo template:

```
# nome e cognome:
# matricola:
#
# path:
#
# comando per abilitare il service:
# comando per avviare il service:
```

### 2. Amministrazione degli account

Configura `sudo` su una rete di quattro host Linux: `edge01`, `edge02`, `core01` e `core02`. La rete ha i seguenti utenti e gruppi:

| Utente | Gruppo primario | Gruppi aggiuntivi |
| ------ | --------------- | ----------------- |
| `sara` | `sara`          |                   |
| `tom`  | `tom`           |                   |
| `uma`  | `uma`           | `ident`           |
| `vera` | `vera`          | `pkg`             |

Applica le seguenti regole:

| Categoria | Regola                                                                                                                                                                          |
| --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Alias     | Definisci `Host_Alias EDGE = edge01, edge02` e `Host_Alias CORE = core01, core02`                                                                                               |
| Alias     | Definisci `Cmnd_Alias EDITORS = /usr/bin/vim, /usr/bin/nano`, `Cmnd_Alias GRPMGM = /usr/sbin/groupadd, /usr/sbin/groupdel` e `Cmnd_Alias PKGINFO = /usr/bin/dpkg, /usr/bin/apt` |
| Permessi  | `sara` può eseguire qualsiasi comando come qualsiasi utente su qualsiasi host                                                                                                   |
| Permessi  | `tom` può eseguire qualsiasi comando come qualsiasi utente su qualsiasi host, eccetto `EDITORS`                                                                                 |
| Permessi  | `%ident` può eseguire `GRPMGM` come `root` su `EDGE`                                                                                                                            |
| Permessi  | `%pkg` può eseguire `PKGINFO` come `root` su `CORE`, senza password                                                                                                             |
| Permessi  | `uma` può eseguire `/usr/bin/cat /etc/sudoers` come `root` su qualsiasi host, senza password                                                                                    |
| Permessi  | `vera` può eseguire `/usr/bin/id` come `tom` su `edge01`                                                                                                                        |
| Permessi  | `%ident, %pkg` può eseguire `/usr/bin/ss` come `root` su qualsiasi host, senza password                                                                                         |

Il file deve essere creato in `/etc/sudoers.d/policy`. Usa questo template:

```
# nome e cognome:
# matricola:
#
# path:
```

### 3. Domande a risposta aperta

1. Quali sono le regole fondamentali che governano il modello tradizionale dei permessi UNIX?
2. Che cos'è un attacco DDoS e come compromette tipicamente i sistemi presi di mira?
3. Quali sono le best practice e le raccomandazioni per creare password sicure, gestire le password in modo efficace e implementare la MFA?

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
| Daemon (§1)                 | 16     |
| - Python script (§1.1)      | 10/16  |
| - Service (§1.2)            | 6/16   |
| Account administration (§2) | 8      |
| Open-ended questions (§3)   | 9      |

To print:

```shell
$ stampa <path/file/to/print>
```

> [!warning]
> 1. Write your **first name**, **last name**, and student id on every file you print.
> 2. After sending the files to the printer, notify the instructor and **remain seated**.

> [!tip]
> 3. If a mistake is spotted on the printed file, it can be corrected by hand.

### 1. Daemon

#### 1.1. Python script

Write a Python script that periodically scans a specified directory (including all its subdirectories) to remove the files whose name starts with a given prefix. In your home directory, create the directory `prefix-cleaner` and, inside it, the file `app.py`, using this template:

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

The script must accept exactly four mandatory command-line arguments, parsed with the `argparse` module: `--target`, which specifies the absolute path of the directory to clean; `--prefix`, which specifies the prefix of the names of the files to remove; `--interval`, which defines the interval in seconds (positive integer) between each check; and `--log`, which specifies the path (absolute or relative) of the directory where to save the log file. The name of the log file is always `prefix-cleaner.log`.

After parsing, validate the received inputs: verify that the path specified with `--target` is absolute (`os.path.isabs`), that it exists (`os.path.exists`), and that it is a directory (`os.path.isdir`); check that the value provided for `--prefix` is non-empty; check that the value provided for `--interval` is a positive integer; verify that the path indicated with `--log` exists (`os.path.exists`) and is a directory (`os.path.isdir`). If any check fails, print an explanatory error message to standard error (`print`) and exit with a non-zero status code (`sys.exit`).

After validation, recursively traverse the directory tree at the path provided with `--target` (`os.listdir`, `os.path.join`, `os.path.isdir`). For each file encountered (`os.path.isfile`), if its name starts with the prefix indicated by `--prefix` (`str.startswith`), open in append mode the log file `prefix-cleaner.log` in the directory specified with `--log` (`open`), write a line containing the current date and time (`datetime.now`), a space, and the absolute path of the file, then remove the file (`os.remove`). The script must repeat this procedure periodically, waiting for a number of seconds equal to the value indicated by `--interval` between each check (`time.sleep`).

For example, running:

```shell
$ python ~/prefix-cleaner/app.py \
    --target ~/scratch \
    --prefix tmp \
    --interval 60 \
    --log ~
```

the script will identify all files whose name starts with `tmp` in `~/scratch` (and in all its subdirectories), append to `~/prefix-cleaner.log` the date, time, and path of each file, and remove those files. The script will repeat the operation every `60` seconds.

#### 1.2. Service

Create a service unit named `prefix-cleaner.service` in your user instance of `systemd`. The unit must start `~/prefix-cleaner/app.py` with the arguments `--target %h/scratch`, `--prefix tmp`, `--interval 60`, and `--log %h`, start at system boot, and restart in case of failures. Use this template:

```
# first and last name:
# student id:
#
# path:
#
# command to enable the service:
# command to start the service:
```

### 2. Account administration

Configure `sudo` on a fleet of four Linux hosts: `edge01`, `edge02`, `core01`, and `core02`. The fleet has the following users and groups:

| User   | Primary group | Additional groups |
| ------ | ------------- | ----------------- |
| `sara` | `sara`        |                   |
| `tom`  | `tom`         |                   |
| `uma`  | `uma`         | `ident`           |
| `vera` | `vera`        | `pkg`             |

Apply the following rules:

| Category    | Rule                                                                                                                                                                            |
| ----------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Aliases     | Define `Host_Alias EDGE = edge01, edge02` and `Host_Alias CORE = core01, core02`                                                                                                |
| Aliases     | Define `Cmnd_Alias EDITORS = /usr/bin/vim, /usr/bin/nano`, `Cmnd_Alias GRPMGM = /usr/sbin/groupadd, /usr/sbin/groupdel`, and `Cmnd_Alias PKGINFO = /usr/bin/dpkg, /usr/bin/apt` |
| Permissions | `sara` can run any command as any user on any host                                                                                                                              |
| Permissions | `tom` can run any command as any user on any host, except `EDITORS`                                                                                                             |
| Permissions | `%ident` can run `GRPMGM` as `root` on `EDGE`                                                                                                                                   |
| Permissions | `%pkg` can run `PKGINFO` as `root` on `CORE`, without a password                                                                                                                |
| Permissions | `uma` can run `/usr/bin/cat /etc/sudoers` as `root` on any host, without a password                                                                                             |
| Permissions | `vera` can run `/usr/bin/id` as `tom` on `edge01`                                                                                                                               |
| Permissions | `%ident, %pkg` can run `/usr/bin/ss` as `root` on any host, without a password                                                                                                  |

The file must be created at `/etc/sudoers.d/policy`. Use this template:

```
# first and last name:
# student id:
#
# path:
```

### 3. Open-ended questions

1. What core rules govern the traditional UNIX permission model?
2. What is a DDoS attack, and how does it typically compromise the targeted systems?
3. What are the best practices and recommendations for creating secure passwords, managing passwords effectively, and implementing MFA?

Use this template:

```
# first and last name:
# student id:

1.

2.

3.
```

## Solutions

- [Daemon (§1)](https://github.com/fglmtt/admin/tree/main/exams/2026-06-08-2/prefix-cleaner)
- [Account administration (§2)](https://github.com/fglmtt/admin/blob/main/exams/2026-06-08-2/sudo)
