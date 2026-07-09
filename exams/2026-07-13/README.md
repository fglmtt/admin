# 13 luglio 2026

Durata esame: 2 ore e 30 minuti.

| Sezione                             | Punti |
| ----------------------------------- | ----- |
| Processo periodico (§1)             | 16    |
| - Script Python (§1.1)              | 8/16  |
| - Service (§1.2)                    | 4/16  |
| - Timer (§1.3)                      | 4/16  |
| Filtraggio dei pacchetti e NAT (§2) | 8     |
| Domande a risposta aperta (§3)      | 9     |

Per stampare:

```shell
$ stampa <path/file/da/stampare>
```

> [!warning]
> 1. Scrivere **nome**, **cognome** e numero di matricola su ogni file che si stampa.
> 2. Una volta mandati in stampa i file, avvisare il docente e **rimanere seduti al posto**.

> [!tip]
> 3. Se si nota un errore sul file stampato, lo si può correggere a penna.

## 1. Processo periodico

### 1.1. Script Python

Scrivi uno script Python che verifica i permessi dei file in una directory specificata e in tutte le sue sottodirectory, registrando in un file di log ogni file i cui permessi non corrispondono esattamente a un valore atteso. Nella tua home directory, crea una directory chiamata `permission-auditor` e, al suo interno, un file chiamato `app.py`, utilizzando questo template:

```python
# nome e cognome:
# matricola:
#
# path: 

import argparse
from datetime import datetime
import os
import stat
import sys

def main():
    pass


if __name__ == "__main__":
    main()
```

Lo script deve accettare esattamente tre argomenti da linea di comando, analizzati con il modulo `argparse`. Il primo argomento, `--path`, è una stringa obbligatoria che indica il percorso assoluto della directory da scansionare. Il secondo argomento, `--mode`, è una stringa obbligatoria che indica i permessi attesi in notazione ottale. Il terzo argomento, `--log`, è una stringa obbligatoria che indica il percorso assoluto del file di log su cui scrivere.

Dopo il parsing, valida gli input: verifica che `--path` sia assoluto (`os.path.isabs`), esista (`os.path.exists`) e sia una directory (`os.path.isdir`); converti `--mode` in un intero interpretandolo come ottale (`int(args.mode, 8)`), intercettando l'eccezione `ValueError` sollevata se non è un numero ottale valido; verifica che `--log` sia un percorso assoluto (`os.path.isabs`). Se uno dei controlli fallisce, stampa un messaggio di errore esplicativo sullo standard error (`print`) ed esci con un codice di stato diverso da zero (`sys.exit`).

Una volta validati, assicurati che la directory che conterrà il file di log esista (`os.path.dirname`, `os.makedirs`). Quindi percorri ricorsivamente l'albero delle directory al percorso fornito come primo argomento (`os.listdir`, `os.path.join`, `os.path.isdir`). Per ogni file incontrato (`os.path.isfile`), estrai i bit dei permessi con `stat.S_IMODE(os.stat('/path/to/file').st_mode)`: `st_mode` contiene anche i bit del tipo di file, quindi `stat.S_IMODE` mantiene solo i bit dei permessi. Se i permessi del file non corrispondono esattamente al valore `--mode`, apri in modalità append il file di log indicato da `--log` (`open`) e scrivi una riga contenente la data e l'ora correnti (`datetime.now`), i permessi del file in notazione ottale (`oct`) e il suo percorso.

Ad esempio, eseguendo:

```shell
$ python ~/permission-auditor/app.py \
    --path ~/data \
    --mode 644 \
    --log ~/permission-auditor.log
```

lo script esaminerà `~/data` e tutte le sue sottodirectory, registrando in `~/permission-auditor.log` ogni file i cui permessi non corrispondono esattamente a `644` (`rw-r--r--`).

### 1.2. Service

Crea un'unità service chiamata `permission-auditor.service` nella tua istanza utente di `systemd`. Configurala per avviare `~/permission-auditor/app.py` con gli argomenti `--path %h/data`, `--mode 644` e `--log %h/permission-auditor.log`. Usa questo template:

```
# nome e cognome:
# matricola:
#
# path: 
```

### 1.3. Timer

Crea un'unità timer chiamata `permission-auditor.timer` nella tua istanza utente di `systemd`. Configurala per attivare `permission-auditor.service` alle 23:30 di ogni martedì e venerdì. Usa questo template:

```
# nome e cognome:
# matricola:
#
# path: 
#
# comando per abilitare il timer:
# comando per avviare il timer:
```

## 2. Filtraggio dei pacchetti e NAT

Configura un firewall Linux utilizzando `iptables`. Il firewall dispone di due interfacce:

| NIC    | Indirizzo di rete | IP del firewall | Ambito   |
| ------ | ----------------- | --------------- | -------- |
| `eth0` | `192.0.2.0/24`    | `192.0.2.1`     | Pubblico |
| `eth1` | `172.20.0.0/24`   | `172.20.0.1`    | Privato  |

Gli host sulla rete `172.20.0.0/24` utilizzano questo firewall come gateway di default. L'host `172.20.0.40` esegue un server SMTP (`tcp/2525`) e un server HTTPS (`tcp/8443`).

Applica le seguenti regole:

| Tabella      | Catena          | Regola                                                                                                                                          |
| ------------ | --------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| `filter,nat` | `*`             | Elimina le regole esistenti                                                                                                                     |
| `filter`     | `INPUT,FORWARD` | Scarta tutto a meno che non sia esplicitamente permesso                                                                                         |
| `filter`     | `INPUT`         | Consenti pacchetti SSH (`tcp/22`) ricevuti su `eth1` e provenienti esclusivamente dall'host amministrativo `172.20.0.90`                        |
| `filter`     | `FORWARD`       | Consenti tutti i pacchetti ricevuti su `eth1` e in uscita su `eth0`                                                                             |
| `filter`     | `FORWARD`       | Consenti pacchetti con stato `ESTABLISHED,RELATED`                                                                                              |
| `nat`        | `POSTROUTING`   | SNAT per i pacchetti in uscita su `eth0` affinché gli host privati ricevano risposte da Internet                                                |
| `nat`        | `PREROUTING`    | DNAT per i pacchetti SMTP (`tcp/25`) ricevuti su `eth0`, inoltrandoli a `172.20.0.40:2525` e assicurandoti che possano raggiungere quell'host   |
| `nat`        | `PREROUTING`    | DNAT per i pacchetti HTTPS (`tcp/443`) ricevuti su `eth0`, inoltrandoli a `172.20.0.40:8443` e assicurandoti che possano raggiungere quell'host |

Usa questo template:

```
# nome e cognome:
# matricola:
```

## 3. Domande a risposta aperta

1. Perché oggi gli amministratori sono tenuti a mantenere un repository di log centralizzato e rafforzato, quale ruolo giocano i timestamp validati tramite NTP, e quali daemon di logging si occupano della raccolta locale rispetto all'inoltro verso il repository centrale?
2. Che cos'è un firewall, come funziona uno schema di filtraggio a due stadi, e quale ruolo svolge una DMZ?
3. Quali sono i limiti di strumenti indiretti come `ps` e i log nell'investigare un processo sospetto, e cosa rivela `strace` che tali strumenti non possono mostrare?

Usa questo template:

```
# nome e cognome:
# matricola:

1.

2.

3.
```

---

# July 13, 2026

Exam duration: 2 hours and 30 minutes.

| Section                       | Points |
| ----------------------------- | ------ |
| Periodic process (§1)         | 16     |
| - Python script (§1.1)        | 8/16   |
| - Service (§1.2)              | 4/16   |
| - Timer (§1.3)                | 4/16   |
| Packet filtering and NAT (§2) | 8      |
| Open-ended questions (§3)     | 9      |

To print:

```shell
$ stampa <path/file/to/print>
```

> [!warning]
> 1. Write your **first name**, **last name**, and student id on every file you print.
> 2. After sending the files to the printer, notify the instructor and **remain seated**.

> [!tip]
> 3. If a mistake is spotted on the printed file, it can be corrected by hand.

## 1. Periodic Process

### 1.1. Python Script

Write a Python script that checks file permissions in a specified directory and all its subdirectories, logging to a log file every file whose permissions do not exactly match an expected mode. In your home directory, create a directory called `permission-auditor` and, inside it, a file called `app.py`, using this template:

```python
# first and last name:
# student id:
#
# path: 

import argparse
from datetime import datetime
import os
import stat
import sys

def main():
    pass


if __name__ == "__main__":
    main()
```

The script must accept exactly three command-line arguments, parsed with the `argparse` module. The first argument, `--path`, is a required string indicating the absolute path of the directory to scan. The second argument, `--mode`, is a required string indicating the expected permissions in octal notation. The third argument, `--log`, is a required string indicating the absolute path of the log file to write to.

After parsing, validate the inputs: check that `--path` is absolute (`os.path.isabs`), exists (`os.path.exists`), and is a directory (`os.path.isdir`); convert `--mode` to an integer by interpreting it as octal (`int(args.mode, 8)`), catching the `ValueError` raised if it is not a valid octal number; check that `--log` is an absolute path (`os.path.isabs`). If any check fails, print an explanatory error message to standard error (`print`) and exit with a non-zero status code (`sys.exit`).

Once validated, ensure that the directory that will contain the log file exists (`os.path.dirname`, `os.makedirs`). Then recursively traverse the directory tree at the path provided as the first argument (`os.listdir`, `os.path.join`, `os.path.isdir`). For each file encountered (`os.path.isfile`), extract its permission bits with `stat.S_IMODE(os.stat('/path/to/file').st_mode)`: `st_mode` also carries the file-type bits, so `stat.S_IMODE` keeps only the permission bits. If the file permissions do not exactly match the `--mode` value, open the log file indicated by `--log` in append mode (`open`) and write a line containing the current date and time (`datetime.now`), the file permissions in octal notation (`oct`), and its path.

For example, running

```shell
$ python ~/permission-auditor/app.py \
    --path ~/data \
    --mode 644 \
    --log ~/permission-auditor.log
```

the script will examine `~/data` and all its subdirectories, logging to `~/permission-auditor.log` every file whose permissions do not exactly match `644` (`rw-r--r--`).

### 1.2. Service

Create a service unit named `permission-auditor.service` in your user instance of `systemd`. Configure it to start `~/permission-auditor/app.py` with the arguments `--path %h/data`, `--mode 644`, and `--log %h/permission-auditor.log`. Use this template:

```
# first and last name:
# student id:
#
# path: 
```

### 1.3. Timer

Create a timer unit named `permission-auditor.timer` in your user instance of `systemd`. Configure it to trigger `permission-auditor.service` at 23:30 on every Tuesday and Friday. Use this template:

```
# first and last name:
# student id:
#
# path: 
#
# command to enable the timer:
# command to start the timer:
```

## 2. Packet filtering and NAT

Configure a Linux firewall using `iptables`. The firewall has two interfaces:

| NIC    | Network Address | Firewall IP  | Scope   |
| ------ | --------------- | ------------ | ------- |
| `eth0` | `192.0.2.0/24`  | `192.0.2.1`  | Public  |
| `eth1` | `172.20.0.0/24` | `172.20.0.1` | Private |

Hosts on the `172.20.0.0/24` network use this firewall as the default gateway. The host `172.20.0.40` runs an SMTP server (`tcp/2525`) and an HTTPS server (`tcp/8443`).

Apply the following rules:

| Table        | Chain           | Rule                                                                                                                               |
| ------------ | --------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| `filter,nat` | `*`             | Clear existing rules                                                                                                               |
| `filter`     | `INPUT,FORWARD` | Drop everything unless explicitly allowed                                                                                          |
| `filter`     | `INPUT`         | Allow SSH packets (`tcp/22`) received on `eth1` and coming exclusively from the administrative host `172.20.0.90`                  |
| `filter`     | `FORWARD`       | Allow all packets received on `eth1` and outgoing on `eth0`                                                                        |
| `filter`     | `FORWARD`       | Allow packets with state `ESTABLISHED,RELATED`                                                                                     |
| `nat`        | `POSTROUTING`   | SNAT for packets outgoing on `eth0` so that private hosts receive responses from the Internet                                      |
| `nat`        | `PREROUTING`    | DNAT for SMTP packets (`tcp/25`) received on `eth0`, forwarding them to `172.20.0.40:2525` and ensuring they can reach that host   |
| `nat`        | `PREROUTING`    | DNAT for HTTPS packets (`tcp/443`) received on `eth0`, forwarding them to `172.20.0.40:8443` and ensuring they can reach that host |

Use this template:

```
# first and last name:
# student id:
```

## 3. Open-ended questions

1. Why are administrators today required to maintain a centralized, hardened logging repository, what role do NTP-validated timestamps play, and which logging daemons handle local collection versus forwarding to the central repository?
2. What is a firewall, how does a two-stage filtering scheme work, and what role does a DMZ play?
3. What are the limitations of indirect tools such as `ps` and logs when investigating a suspicious process, and what does `strace` reveal that they cannot?

Use this template:

```
# first and last name:
# student id:

1.

2.

3.
```
