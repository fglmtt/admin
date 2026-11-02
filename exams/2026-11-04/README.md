# November 4, 2026

## Italian

Durata esame: 2 ore e 30 minuti.

| Sezione                             | Punti |
| ----------------------------------- | ----- |
| Demone (§1)                         | 16    |
| - Script Python (§1.1)              | 10/16 |
| - Service (§1.2)                    | 6/16  |
| Filtraggio dei pacchetti e NAT (§2) | 8     |
| Domande a risposta aperta (§3)      | 9     |

Per consegnare, vai su <https://esami.unife.it/>.

### 1. Demone

#### 1.1. Script Python

Scrivi uno script Python che periodicamente analizza una directory specificata (incluse tutte le sue sottodirectory) per individuare i file di proprietà di un determinato insieme di utenti. Nella tua home directory, crea la directory `owner-detector` e, al suo interno, il file `app.py`, utilizzando questo template:

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

Lo script deve accettare esattamente quattro argomenti obbligatori da linea di comando, analizzati con il modulo `argparse`: `--target`, che indica il percorso assoluto della directory da analizzare; `--users`, che specifica un elenco di user ID (UID), separati da virgole, di cui individuare i file; `--interval`, che definisce l'intervallo in secondi (intero positivo) tra ogni controllo; e `--log`, che indica il percorso assoluto del file di log.

Dopo il parsing, valida gli input ricevuti: verifica che il percorso specificato con `--target` sia assoluto (`os.path.isabs`), che esista (`os.path.exists`) e che sia una directory (`os.path.isdir`); suddividi il valore fornito per `--users` sulle virgole (`str.split`) e controlla che ogni elemento ottenuto sia un intero non negativo (`int`); controlla che il valore fornito per `--interval` sia un intero positivo; verifica che il percorso indicato con `--log` sia assoluto (`os.path.isabs`) e che la directory che lo conterrà esista (`os.path.dirname`, `os.path.exists`) e sia una directory (`os.path.isdir`). Se un controllo fallisce, stampa un messaggio di errore esplicativo sullo standard error (`print`) ed esci con un codice di stato diverso da zero (`sys.exit`).

Dopo la validazione, percorri ricorsivamente l'albero delle directory al percorso fornito con `--target` (`os.listdir`, `os.path.join`, `os.path.isdir`). Per ogni file incontrato (`os.path.isfile`), ricava l'UID del suo proprietario (`os.stat(path).st_uid`). Se tale UID è tra quelli indicati da `--users`, scrivi nel file di log indicato da `--log` (`open`) una riga contenente data e ora corrente (`datetime.now`), uno spazio, il percorso assoluto del file, uno spazio e l'UID del suo proprietario. A ogni controllo, il file di log deve essere sovrascritto, così che contenga solo i file individuati dal controllo più recente. Lo script non deve modificare nessun altro file. Assumi che il file di log non si trovi nella directory specificata con `--target` né in una delle sue sottodirectory. Lo script deve ripetere questa procedura periodicamente, attendendo un numero di secondi pari al valore indicato da `--interval` tra ciascun controllo (`time.sleep`).

Ad esempio, eseguendo:

```shell
$ python ~/owner-detector/app.py \
    --target ~/shared \
    --users 0,1000 \
    --interval 60 \
    --log ~/owner-detector.log
```

lo script individuerà tutti i file di proprietà degli utenti con UID `0` (`root`) o `1000` presenti in `~/shared` (e in tutte le sue sottodirectory), e scriverà in `~/owner-detector.log` la data, l'ora, il percorso e l'UID del proprietario di ciascun file, sovrascrivendo il log a ogni controllo. Lo script ripeterà l'operazione ogni `60` secondi. Per conoscere il tuo UID, esegui `id -u`.

#### 1.2. Service

Crea un'unità service denominata `owner-detector.service` nella tua istanza utente di `systemd`. L'unità deve avviare `~/owner-detector/app.py` con gli argomenti `--target %h/shared`, `--users 0,1000`, `--interval 60` e `--log %h/owner-detector.log`, partire all'avvio del sistema e ripartire in caso di fallimenti. Usa questo template:

```
# nome e cognome:
# matricola:
#
# path:
#
# comando per abilitare il service:
# comando per avviare il service:
```

### 2. Filtraggio dei pacchetti e NAT

Configura un firewall Linux utilizzando `iptables`. Il firewall dispone di due interfacce:

| NIC    | Indirizzo di rete | IP del firewall | Ambito   |
| ------ | ----------------- | --------------- | -------- |
| `eth0` | `198.51.100.0/24` | `198.51.100.20` | Pubblico |
| `eth1` | `10.50.0.0/24`    | `10.50.0.1`     | Privato  |

Gli host sulla rete `10.50.0.0/24` utilizzano questo firewall come gateway di default. L'host `10.50.0.25` esegue un server SSH (`tcp/22`).

Applica le seguenti regole:

| Tabella      | Catena          | Regola                                                                                                                                   |
| ------------ | --------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| `filter,nat` | `*`             | Elimina le regole esistenti                                                                                                              |
| `filter`     | `INPUT,FORWARD` | Scarta tutto a meno che non sia esplicitamente permesso                                                                                  |
| `filter`     | `INPUT`         | Consenti pacchetti ICMP ricevuti su `eth1` e provenienti esclusivamente dall'host amministrativo `10.50.0.200`                           |
| `filter`     | `INPUT`         | Consenti pacchetti SSH (`tcp/22`) ricevuti su `eth1` e provenienti esclusivamente dall'host amministrativo `10.50.0.200`                 |
| `filter`     | `FORWARD`       | Consenti pacchetti DNS (`udp/53`) e HTTPS (`tcp/443`) ricevuti su `eth1` e in uscita su `eth0`                                           |
| `filter`     | `FORWARD`       | Consenti pacchetti con stato `ESTABLISHED,RELATED`                                                                                       |
| `nat`        | `POSTROUTING`   | MASQUERADE per i pacchetti in uscita su `eth0` affinché gli host privati ricevano risposte da Internet                                   |
| `nat`        | `PREROUTING`    | DNAT per i pacchetti su `tcp/2222` ricevuti su `eth0`, inoltrandoli a `10.50.0.25:22` e assicurandoti che possano raggiungere quell'host |

Usa questo template:

```
# nome e cognome:
# matricola:
```

### 3. Domande a risposta aperta

1. Che cos'è l'IPv4 source routing e in che modo un attaccante può sfruttarlo?
2. Che cosa sono i virus e i worm informatici e quali sono le principali differenze tra questi due tipi di malware?
3. Che cos'è la crittografia a chiave pubblica, come funziona e quali sono i suoi principali vantaggi e svantaggi?

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

| Section                       | Points |
| ----------------------------- | ------ |
| Daemon (§1)                   | 16     |
| - Python script (§1.1)        | 10/16  |
| - Service (§1.2)              | 6/16   |
| Packet filtering and NAT (§2) | 8      |
| Open-ended questions (§3)     | 9      |

To submit, go to <https://esami.unife.it/>.

### 1. Daemon

#### 1.1. Python script

Write a Python script that periodically scans a specified directory (including all its subdirectories) to detect the files owned by a given set of users. In your home directory, create the directory `owner-detector` and, inside it, the file `app.py`, using this template:

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

The script must accept exactly four mandatory command-line arguments, parsed with the `argparse` module: `--target`, which specifies the absolute path of the directory to scan; `--users`, which specifies a comma-separated list of user IDs (UIDs) whose files must be detected; `--interval`, which defines the interval in seconds (positive integer) between each check; and `--log`, which specifies the absolute path of the log file.

After parsing, validate the received inputs: verify that the path specified with `--target` is absolute (`os.path.isabs`), that it exists (`os.path.exists`), and that it is a directory (`os.path.isdir`); split the value provided for `--users` on commas (`str.split`) and check that each resulting item is a non-negative integer (`int`); check that the value provided for `--interval` is a positive integer; verify that the path indicated with `--log` is absolute (`os.path.isabs`) and that the directory that will contain it exists (`os.path.dirname`, `os.path.exists`) and is a directory (`os.path.isdir`). If any check fails, print an explanatory error message to standard error (`print`) and exit with a non-zero status code (`sys.exit`).

After validation, recursively traverse the directory tree at the path provided with `--target` (`os.listdir`, `os.path.join`, `os.path.isdir`). For each file encountered (`os.path.isfile`), retrieve the UID of its owner (`os.stat(path).st_uid`). If that UID is one of those indicated by `--users`, write to the log file indicated by `--log` (`open`) a line containing the current date and time (`datetime.now`), a space, the absolute path of the file, a space, and the UID of its owner. At every check, the log file must be overwritten, so that it contains only the files detected by the most recent check. The script must not modify any other file. Assume that the log file is not inside the directory specified with `--target` or any of its subdirectories. The script must repeat this procedure periodically, waiting for a number of seconds equal to the value indicated by `--interval` between each check (`time.sleep`).

For example, running:

```shell
$ python ~/owner-detector/app.py \
    --target ~/shared \
    --users 0,1000 \
    --interval 60 \
    --log ~/owner-detector.log
```

the script will identify all files owned by the users with UID `0` (`root`) or `1000` in `~/shared` (and in all its subdirectories), and write to `~/owner-detector.log` the date, time, path, and owner UID of each file, overwriting the log at every check. The script will repeat the operation every `60` seconds. To find your own UID, run `id -u`.

#### 1.2. Service

Create a service unit named `owner-detector.service` in your user instance of `systemd`. The unit must start `~/owner-detector/app.py` with the arguments `--target %h/shared`, `--users 0,1000`, `--interval 60`, and `--log %h/owner-detector.log`, start at system boot, and restart in case of failures. Use this template:

```
# first and last name:
# student id:
#
# path:
#
# command to enable the service:
# command to start the service:
```

### 2. Packet filtering and NAT

Configure a Linux firewall using `iptables`. The firewall has two interfaces:

| NIC    | Network address   | Firewall IP     | Scope   |
| ------ | ----------------- | --------------- | ------- |
| `eth0` | `198.51.100.0/24` | `198.51.100.20` | Public  |
| `eth1` | `10.50.0.0/24`    | `10.50.0.1`     | Private |

Hosts on the `10.50.0.0/24` network use this firewall as the default gateway. The host `10.50.0.25` runs an SSH server (`tcp/22`).

Apply the following rules:

| Table        | Chain           | Rule                                                                                                                        |
| ------------ | --------------- | --------------------------------------------------------------------------------------------------------------------------- |
| `filter,nat` | `*`             | Clear existing rules                                                                                                        |
| `filter`     | `INPUT,FORWARD` | Drop everything unless explicitly allowed                                                                                   |
| `filter`     | `INPUT`         | Allow ICMP packets received on `eth1` and coming exclusively from the administrative host `10.50.0.200`                     |
| `filter`     | `INPUT`         | Allow SSH packets (`tcp/22`) received on `eth1` and coming exclusively from the administrative host `10.50.0.200`           |
| `filter`     | `FORWARD`       | Allow DNS (`udp/53`) and HTTPS (`tcp/443`) packets received on `eth1` and outgoing on `eth0`                                |
| `filter`     | `FORWARD`       | Allow packets with state `ESTABLISHED,RELATED`                                                                              |
| `nat`        | `POSTROUTING`   | MASQUERADE packets outgoing on `eth0` so that private hosts receive responses from the Internet                             |
| `nat`        | `PREROUTING`    | DNAT for packets on `tcp/2222` received on `eth0`, forwarding them to `10.50.0.25:22` and ensuring they can reach that host |

Use this template:

```
# first and last name:
# student id:
```

### 3. Open-ended questions

1. What is IPv4 source routing, and how can an attacker exploit it?
2. What are computer viruses and worms, and what are the key differences between these two types of malware?
3. What is public key cryptography, how does it work, and what are its primary advantages and disadvantages?

Use this template:

```
# first and last name:
# student id:

1.

2.

3.
```

## Solutions

- [Daemon (§1)](https://github.com/fglmtt/admin/tree/main/exams/2026-11-04/owner-detector)
- [Packet filtering and NAT (§2)](https://github.com/fglmtt/admin/blob/main/exams/2026-11-04/iptables)
