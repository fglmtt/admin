# June 8, 2026 - Session 1

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

Scrivi uno script Python che periodicamente conta i file con una determinata estensione presenti in una directory specificata (incluse tutte le sue sottodirectory) e registra nel file di log la data, l'ora, l'estensione e il numero di file contati. Nella tua home directory, crea la directory `extension-counter` e, al suo interno, il file `app.py`, utilizzando questo template:

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

Lo script deve accettare esattamente quattro argomenti obbligatori da linea di comando, analizzati con il modulo `argparse`: `--target`, che indica il percorso assoluto della directory da monitorare; `--ext`, che specifica l'estensione dei file da contare, punto iniziale incluso (ad esempio `.log`); `--interval`, che definisce l'intervallo in secondi (intero positivo) tra ogni controllo; e `--log`, che indica il percorso (assoluto o relativo) della directory dove salvare il file di log. Il nome del file di log è sempre `extension-counter.log`.

Dopo il parsing, valida gli input ricevuti: verifica che il percorso specificato con `--target` sia assoluto (`os.path.isabs`), che esista (`os.path.exists`) e che sia una directory (`os.path.isdir`); controlla che il valore fornito per `--ext` non sia vuoto e inizi con un punto (`str.startswith`); controlla che il valore fornito per `--interval` sia un intero positivo; verifica che il percorso indicato con `--log` esista (`os.path.exists`) e sia una directory (`os.path.isdir`). Se un controllo fallisce, stampa un messaggio di errore esplicativo sullo standard error (`print`) ed esci con un codice di stato diverso da zero (`sys.exit`).

Dopo la validazione, percorri ricorsivamente l'albero delle directory al percorso fornito con `--target` (`os.listdir`, `os.path.join`, `os.path.isdir`). Per ogni file incontrato (`os.path.isfile`), ottieni la sua estensione (`os.path.splitext`) e, se coincide esattamente con il valore indicato da `--ext`, incrementa un contatore. Il confronto tra estensioni è case-sensitive (`.log` è diverso da `.LOG`). Al termine della visita, apri in modalità append il file di log `extension-counter.log` nella directory specificata con `--log` (`open`) e scrivi una riga contenente data e ora corrente (`datetime.now`), uno spazio, l'estensione, uno spazio e il numero di file contati. Lo script deve ripetere questa procedura periodicamente, attendendo un numero di secondi pari al valore indicato da `--interval` tra ciascun controllo (`time.sleep`).

Ad esempio, eseguendo:

```shell
$ python ~/extension-counter/app.py \
    --target ~/documents \
    --ext .log \
    --interval 60 \
    --log ~
```

lo script conterà tutti i file con estensione `.log` presenti in `~/documents` (e in tutte le sue sottodirectory) e scriverà in append in `~/extension-counter.log` la data, l'ora, l'estensione e il numero di file contati. Lo script ripeterà l'operazione ogni `60` secondi.

#### 1.2. Service

Crea un'unità service denominata `extension-counter.service` nella tua istanza utente di `systemd`. L'unità deve avviare `~/extension-counter/app.py` con gli argomenti `--target %h/documents`, `--ext .log`, `--interval 60`, e `--log %h`, partire all'avvio del sistema e ripartire in caso di fallimenti. Usa questo template:

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

Configura `sudo` su una rete di tre host Linux: `runner01`, `runner02` e `registry01`. La rete ha i seguenti utenti e gruppi:

| Utente  | Gruppo primario | Gruppi aggiuntivi |
| ------- | --------------- | ----------------- |
| `nora`  | `nora`          |                   |
| `omar`  | `omar`          |                   |
| `priya` | `priya`         | `dev`             |
| `quinn` | `quinn`         | `sec`             |
| `ravi`  | `ravi`          | `ops`             |

Applica le seguenti regole:

| Categoria | Regola                                                                                                                                                                                         |
| --------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Alias     | Definisci `Host_Alias RUNNERS = runner01, runner02`                                                                                                                                            |
| Alias     | Definisci `Cmnd_Alias USERMGM = /usr/sbin/useradd, /usr/sbin/userdel, /usr/sbin/usermod`, `Cmnd_Alias NETINFO = /usr/bin/ip, /usr/bin/ss` e `Cmnd_Alias PKGINFO = /usr/bin/dpkg, /usr/bin/apt` |
| Permessi  | `nora` può eseguire qualsiasi comando come qualsiasi utente su qualsiasi host                                                                                                                  |
| Permessi  | `omar` può eseguire qualsiasi comando come qualsiasi utente su qualsiasi host, eccetto `USERMGM`                                                                                               |
| Permessi  | `%dev` può eseguire `NETINFO` come `root` su `RUNNERS`                                                                                                                                         |
| Permessi  | `%sec` può eseguire `PKGINFO` come `root` su `registry01`, senza password                                                                                                                      |
| Permessi  | `priya` può eseguire `/usr/bin/cat /etc/shadow` come `root` su qualsiasi host, senza password                                                                                                  |
| Permessi  | `quinn` può eseguire `/usr/bin/id` come `ravi` su `RUNNERS`                                                                                                                                    |
| Permessi  | `%ops, %dev` può eseguire `/usr/bin/tcpdump` come `root` su qualsiasi host, senza password                                                                                                     |

Il file deve essere creato in `/etc/sudoers.d/fleet`. Usa questo template:

```
# nome e cognome:
# matricola:
#
# path:
```

### 3. Domande a risposta aperta

1. Che cos'è l'esecuzione set-UID, perché `passwd` ne ha bisogno e cosa accade quando un utente normale esegue `passwd`?
2. Perché mantenere i sistemi aggiornati con le patch è considerato il compito di sicurezza di maggior valore per l'amministratore, quali rischi introducono le patch stesse e cosa dovrebbe includere una procedura di patching adeguata?
3. Che cos'è un rootkit, come funziona tipicamente e perché può essere particolarmente difficile da rilevare e rimuovere?

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

Write a Python script that periodically counts the files with a given extension in a specified directory (including all its subdirectories) and logs the date, time, extension, and number of files counted. In your home directory, create the directory `extension-counter` and, inside it, the file `app.py`, using this template:

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

The script must accept exactly four mandatory command-line arguments, parsed with the `argparse` module: `--target`, which specifies the absolute path of the directory to monitor; `--ext`, which specifies the extension of the files to count, leading dot included (for example `.log`); `--interval`, which defines the interval in seconds (positive integer) between each check; and `--log`, which specifies the path (absolute or relative) of the directory where to save the log file. The name of the log file is always `extension-counter.log`.

After parsing, validate the received inputs: verify that the path specified with `--target` is absolute (`os.path.isabs`), that it exists (`os.path.exists`), and that it is a directory (`os.path.isdir`); check that the value provided for `--ext` is non-empty and starts with a dot (`str.startswith`); check that the value provided for `--interval` is a positive integer; verify that the path indicated with `--log` exists (`os.path.exists`) and is a directory (`os.path.isdir`). If any check fails, print an explanatory error message to standard error (`print`) and exit with a non-zero status code (`sys.exit`).

After validation, recursively traverse the directory tree at the path provided with `--target` (`os.listdir`, `os.path.join`, `os.path.isdir`). For each file encountered (`os.path.isfile`), get its extension (`os.path.splitext`) and, if it matches exactly the value indicated by `--ext`, increment a counter. The extension comparison is case-sensitive (`.log` is different from `.LOG`). At the end of the traversal, open in append mode the log file `extension-counter.log` in the directory specified with `--log` (`open`) and write a line containing the current date and time (`datetime.now`), a space, the extension, a space, and the number of files counted. The script must repeat this procedure periodically, waiting for a number of seconds equal to the value indicated by `--interval` between each check (`time.sleep`).

For example, running:

```shell
$ python ~/extension-counter/app.py \
    --target ~/documents \
    --ext .log \
    --interval 60 \
    --log ~
```

the script will count all files with the `.log` extension in `~/documents` (and in all its subdirectories) and will append to `~/extension-counter.log` the date, time, extension, and number of files counted. The script will repeat the operation every `60` seconds.

#### 1.2. Service

Create a service unit named `extension-counter.service` in your user instance of `systemd`. The unit must start `~/extension-counter/app.py` with the arguments `--target %h/documents`, `--ext .log`, `--interval 60`, and `--log %h`, start at system boot, and restart in case of failures. Use this template:

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

Configure `sudo` on a fleet of three Linux hosts: `runner01`, `runner02`, and `registry01`. The fleet has the following users and groups:

| User    | Primary group | Additional groups |
| ------- | ------------- | ----------------- |
| `nora`  | `nora`        |                   |
| `omar`  | `omar`        |                   |
| `priya` | `priya`       | `dev`             |
| `quinn` | `quinn`       | `sec`             |
| `ravi`  | `ravi`        | `ops`             |

Apply the following rules:

| Category    | Rule                                                                                                                                                                                           |
| ----------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Aliases     | Define `Host_Alias RUNNERS = runner01, runner02`                                                                                                                                               |
| Aliases     | Define `Cmnd_Alias USERMGM = /usr/sbin/useradd, /usr/sbin/userdel, /usr/sbin/usermod`, `Cmnd_Alias NETINFO = /usr/bin/ip, /usr/bin/ss`, and `Cmnd_Alias PKGINFO = /usr/bin/dpkg, /usr/bin/apt` |
| Permissions | `nora` can run any command as any user on any host                                                                                                                                             |
| Permissions | `omar` can run any command as any user on any host, except `USERMGM`                                                                                                                           |
| Permissions | `%dev` can run `NETINFO` as `root` on `RUNNERS`                                                                                                                                                |
| Permissions | `%sec` can run `PKGINFO` as `root` on `registry01`, without a password                                                                                                                         |
| Permissions | `priya` can run `/usr/bin/cat /etc/shadow` as `root` on any host, without a password                                                                                                           |
| Permissions | `quinn` can run `/usr/bin/id` as `ravi` on `RUNNERS`                                                                                                                                           |
| Permissions | `%ops, %dev` can run `/usr/bin/tcpdump` as `root` on any host, without a password                                                                                                              |

The file must be created at `/etc/sudoers.d/fleet`. Use this template:

```
# first and last name:
# student id:
#
# path:
```

### 3. Open-ended questions

1. What is set-UID execution, why does `passwd` need it, and what happens when a regular user runs `passwd`?
2. Why is keeping systems patched considered the administrator's highest-value security chore, what risks do patches themselves introduce, and what should a sound patching procedure include?
3. What is a rootkit, how does it typically function, and why can it be particularly challenging to detect and remove?

Use this template:

```
# first and last name:
# student id:

1.

2.

3.
```

## Solutions

- [Daemon (§1)](https://github.com/fglmtt/admin/tree/main/exams/2026-06-08-1/extension-counter)
- [Account administration (§2)](https://github.com/fglmtt/admin/blob/main/exams/2026-06-08-1/sudo)
