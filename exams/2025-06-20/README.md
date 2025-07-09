# 20 giugno 2025

Durata esame: 2 ore e 30 minuti

| Sezione                             | Punti |
| ----------------------------------- | ----- |
| Demone (§1)                         | 16    |
| - Script Python (§1.1)              | 10/16 |
| - Service (§1.2)                    | 6/16  |
| Filtraggio dei pacchetti e NAT (§2) | 8     |
| Domande a risposta aperta (§3)      | 9     |

Per stampare

```shell
$ stampa <path/file/da/stampare>
```

> [!warning]
> 1. Scrivere **nome**, **cognome** e numero di matricola su ogni file che si stampa
> 2. Una volta mandati in stampa i file, avvisare il docente e **rimanere seduti al posto**

> [!tip]
> 1. Se si nota un errore sul file stampato, lo si può correggere a penna

## 1. Demone

### 1.1. Script Python

Scrivi uno script Python che periodicamente analizza una directory specificata (incluse tutte le sue sottodirectory) identificando i file la cui dimensione supera o eguaglia una certa soglia (in byte). Ogniqualvolta lo script trova un file la cui dimensione è maggiore o uguale alla soglia deve scrivere il percorso di quel file in un file di log. Nella tua home directory, crea la directory `large-file-detector` e, al suo interno, il file `app.py`, utilizzando questo template:

```python
# nome e cognome:
# matricola:
#
# path:

import argparse
import os
import sys
import time

def main():
    pass


if __name__ == "__main__":
    main()
```

Lo script deve accettare esattamente quattro argomenti obbligatori da linea di comando, analizzati con il modulo `argparse`: `--target`, che indica il percorso assoluto della directory da controllare; `--size`, che specifica la dimensione minima in byte (intero positivo) dei file da segnalare; `--interval`, che definisce l'intervallo in secondi (intero positivo) tra ogni controllo; e infine `--log`, che indica dove salvare il file di log. Il nome del file di log è sempre `large-file-detector.log`.

Dopo il parsing, valida gli input ricevuti: verifica che il percorso specificato con `--target` sia assoluto (`os.path.isabs`), che esista (`os.path.exists`) e che sia una directory (`os.path.isdir`); controlla inoltre che i valori forniti per `--size` e `--interval` siano interi positivi; verifica che il percorso indicato con `--log` esista (`os.path.exists`) e sia una directory (`os.path.isdir`).

Dopo la validazione, percorri quindi ricorsivamente l'albero delle directory al percorso fornito con `--target` (`os.listdir`, `os.path.join`, `os.path.isdir`). Per ogni file (`os.path.isfile`), calcola la sua dimensione (`os.path.getsize`) e confrontala con la soglia definita da `--size`. Se la dimensione è maggiore o uguale alla soglia indicata, scrivi il percorso assoluto del file, seguito da un newline, nel file di log chiamato `large-file-detector.log` (`open`), posizionato nella directory specificata con `--log`. Ogni operazione di scrittura nel file di log deve essere fatta in modalità append. Lo script deve ripetere questa procedura periodicamente, attendendo un numero di secondi pari al valore indicato da `--interval` tra ciascun controllo (`time.sleep`).

Ad esempio, eseguendo

```shell
$ python ~/large-file-detector/app.py \
    --target ~/archive \
    --size 10 \
    --interval 30 \
    --log ~
```

lo script dovrà individuare tutti i file di `10` byte o più presenti in `~/archive` (e in tutte le sue sottodirectory) e scrivere in append in `~/large-file-detector.log` il percorso di ciascuno dei file individuati. Lo script ripeterà l'operazione ogni `30` secondi.

### 1.2. Service

Crea un’unità *service* denominata `large-file-detector.service` nella tua istanza utente di `systemd`. L'unità deve avviare `~/large-file-detector/app.py` con gli argomenti `--target %h/docs`, `--size 100`, `--interval 300`, e `--log %h`, partire all'avvio del sistema e ripartire in caso di fallimenti. Usa questo template:

```
# nome e cognome:
# matricola:
#
# path: 
# 
# comando per abilitare il servizio:
# comando per avviare il servizio:
```

## 2. Filtraggio dei pacchetti e NAT

Configura un firewall Linux utilizzando `iptables`. Il firewall ha due interfacce:

| NIC    | Indirizzo di rete | IP del firewall | Ambito   |
| ------ | ----------------- | --------------- | -------- |
| `eth0` | `198.51.100.0/24` | `198.51.100.5`  | Pubblico |
| `eth1` | `10.10.20.0/24`   | `10.10.20.1`    | Privato  |

Gli host della rete `10.10.20.0/24` utilizzano il firewall come gateway predefinito. L'host `10.10.20.50` esegue un server FTP sulla porta `19990`.

Applica le seguenti regole:

| Tabella      | Catena          | Regola                                                                                           |
| ------------ | --------------- | ------------------------------------------------------------------------------------------------ |
| `filter,nat` | `*`             | Elimina tutte le regole esistenti                                                                |
| `filter`     | `INPUT,FORWARD` | Scarta tutto a meno che non sia esplicitamente permesso                                          |
| `filter`     | `INPUT`         | Consenti pacchetti ICMP ricevuti su `eth0` e `eth1`                                              |
| `filter`     | `INPUT`         | Consenti pacchetti SSH (`tcp/22`) ricevuti su `eth1`                                             |
| `filter`     | `FORWARD`       | Consenti tutti i pacchetti ricevuti su `eth1` e in uscita su `eth0`                              |
| `filter`     | `FORWARD`       | Consenti pacchetti con stato `ESTABLISHED,RELATED`                                               |
| `nat`        | `POSTROUTING`   | MASQUERADE pacchetti in uscita da `eth0` affinché gli host privati ricevano risposte da Internet |
| `nat`        | `PREROUTING`    | Applica DNAT ai pacchetti FTPS (`tcp/990`) ricevuti su `eth0` inoltrandoli a `10.10.20.50:19990` |

Usa questo template:

```
# nome e cognome:
# matricola:
```

## 3. Domande a risposta aperta

1. Chi può modificare l'ownership di un file (owner e group owner), quali regole devono essere soddisfatte e quale comando esegue l'operazione?
2. Cos'è l'ingegneria sociale, perché è particolarmente difficile da contrastare e qual è una forma comune di questo tipo di attacco?
3. Qual è la differenza tra un attacco DoS e un attacco DDoS, e come questi attacchi generalmente compromettono i sistemi presi di mira?

Usa questo template:

```
# nome e cognome:
# matricola:

1.

2.

3.
```

---

# June 20, 2025

Exam duration: 2 hours and 30 minutes

| Section                       | Points |
| ----------------------------- | ------ |
| Daemon (§1)                   | 16     |
| - Python script (§1.1)        | 10/16  |
| - Service (§1.2)              | 6/16   |
| Packet filtering and NAT (§2) | 8      |
| Open-ended questions (§3)     | 9      |

To print

```shell
$ stampa <path/file/to/print>
```

> [!warning]
> 1. Write your **first name**, **last name**, and student id on every file you print
> 2. After sending the files to the printer, notify the instructor and **remain seated**

> [!tip]
> 1. If a mistake is spotted on the printed file, it can be corrected by hand

## 1. Daemon

### 1.1. Python script

Write a Python script that periodically analyzes a specified directory (including all its subdirectories), identifying files whose size exceeds or equals a certain threshold (in bytes). Whenever the script finds a file whose size is greater than or equal to the threshold, it must write the file's path to a log file. In your home directory, create a directory called `large-file-detector`, and inside it, the file `app.py`, using this template:

```python
# first name and last name:
# student id:
#
# path:

import argparse
import os
import sys
import time

def main():
    pass


if __name__ == "__main__":
    main()
```

The script must accept exactly four mandatory command-line arguments, parsed with the `argparse` module: `--target`, indicating the absolute path of the directory to check; `--size`, specifying the minimum size in bytes (positive integer) of files to report; `--interval`, defining the interval in seconds (positive integer) between each check; and finally, `--log`, specifying where to save the log file. The log file's name is always `large-file-detector.log`.

After parsing, validate the received inputs: check that the path specified by `--target` is absolute (`os.path.isabs`), exists (`os.path.exists`), and is a directory (`os.path.isdir`); also check that the values provided for `--size` and `--interval` are positive integers; verify that the path indicated by `--log` exists (`os.path.exists`) and is a directory (`os.path.isdir`).

After validation, recursively traverse the directory tree at the path provided with `--target` (`os.listdir`, `os.path.join`, `os.path.isdir`). For each file (`os.path.isfile`), compute its size (`os.path.getsize`) and compare it with the threshold defined by `--size`. If the size is greater than or equal to the indicated threshold, write the absolute path of the file, followed by a newline, into the log file named `large-file-detector.log` (`open`), located in the directory specified with `--log`. Each write operation to the log file must be in append mode. The script must repeat this procedure periodically, waiting a number of seconds equal to the value indicated by `--interval` between each check (`time.sleep`).

For example, running

```shell
$ python ~/large-file-detector/app.py \
    --target ~/archive \
    --size 10 \
    --interval 30 \
    --log ~
```

the script will identify all files of `10` bytes or more in `~/archive` (and all its subdirectories) and append the path of each identified file to `~/large-file-detector.log`. The script will repeat this operation every `30` seconds.

### 1.2. Service

Create a service unit named `large-file-detector.service` in your user's `systemd` instance. The unit must start `~/large-file-detector/app.py` with the arguments `--target %h/docs`, `--size 100`, `--interval 300`, and `--log %h`, start at system boot, and restart in case of failures. Use this template:

```
# first name and last name:
# student id:
#
# path: 
# 
# command to enable the service:
# command to start the service:
```

## 2. Packet filtering and NAT

Configure a Linux firewall using `iptables`. The firewall has two interfaces:

| NIC    | Network Address     | Firewall IP     | Scope    |
| ------ | ------------------- | --------------- | -------- |
| `eth0` | `198.51.100.0/24`   | `198.51.100.5`  | Public   |
| `eth1` | `10.10.20.0/24`     | `10.10.20.1`    | Private  |

Hosts on the `10.10.20.0/24` network use the firewall as their default gateway. Host `10.10.20.50` runs an FTP server on port `19990`.

Apply the following rules:

| Table        | Chain           | Rule                                                                                              |
| ------------ | --------------- | ------------------------------------------------------------------------------------------------- |
| `filter,nat` | `*`             | Flush all existing rules                                                                          |
| `filter`     | `INPUT,FORWARD` | Drop everything unless explicitly allowed                                                         |
| `filter`     | `INPUT`         | Allow ICMP packets received on `eth0` and `eth1`                                                  |
| `filter`     | `INPUT`         | Allow SSH packets (`tcp/22`) received on `eth1`                                                   |
| `filter`     | `FORWARD`       | Allow all packets received on `eth1` and outgoing on `eth0`                                       |
| `filter`     | `FORWARD`       | Allow packets with `ESTABLISHED,RELATED` state                                                    |
| `nat`        | `POSTROUTING`   | MASQUERADE packets going out through `eth0` so private hosts receive replies from the Internet    |
| `nat`        | `PREROUTING`    | Apply DNAT to FTPS packets (`tcp/990`) received on `eth0`, forwarding them to `10.10.20.50:19990` |

Use this template:

```
# first and last name:
# student id:
```

## 3. Open-ended questions

1. Who may change a file’s ownership (owner and group owner), what rules must be satisfied, and which command performs the operation?
2. What is social engineering, why is it particularly difficult to defend against, and what is one common form of this attack?
3. What is the difference between a DoS attack and a DDoS attack, and how do these attacks typically compromise the targeted systems?

Use this template:

```
# first and last name:
# student id:

1.

2.

3.
```
