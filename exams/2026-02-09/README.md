# 9 febbraio 2026

Durata esame: 2 ore e 30 minuti.

| Sezione                             | Punti |
| ----------------------------------- | ----- |
| Demone (§1)                         | 16    |
| - Script Python (§1.1)              | 10/16 |
| - Service (§1.2)                    | 6/16  |
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

## 1. Demone

### 1.1. Script Python

Scrivi uno script Python che periodicamente calcola la dimensione totale di tutti i file presenti in una directory specificata (incluse tutte le sue sottodirectory) e registra nel file di log la data, l'ora e la dimensione totale quando questa supera una certa soglia espressa in byte. Nella tua home directory, crea la directory `dir-size-monitor` e, al suo interno, il file `app.py`, utilizzando questo template:

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

Lo script deve accettare esattamente quattro argomenti obbligatori da linea di comando, analizzati con il modulo `argparse`: `--target`, che indica il percorso assoluto della directory da monitorare; `--threshold`, che specifica la soglia in byte (intero positivo) oltre la quale deve essere registrato un avviso; `--interval`, che definisce l'intervallo in secondi (intero positivo) tra ogni controllo; e `--log`, che indica il percorso assoluto della directory dove salvare il file di log. Il nome del file di log è sempre `dir-size-monitor.log`.

Dopo il parsing, valida gli input ricevuti: verifica che il percorso specificato con `--target` sia assoluto (`os.path.isabs`), che esista (`os.path.exists`) e che sia una directory (`os.path.isdir`); controlla inoltre che i valori forniti per `--threshold` e `--interval` siano interi positivi; verifica che il percorso indicato con `--log` esista, sia una directory e sia assoluto. Se un controllo fallisce, stampa un messaggio di errore esplicativo sullo standard error (`print`) ed esci con un codice di stato diverso da zero (`sys.exit`).

Dopo la validazione, percorri ricorsivamente l'albero delle directory al percorso fornito con `--target` (`os.listdir`, `os.path.join`, `os.path.isdir`). Per ogni file incontrato (`os.path.isfile`), ottieni la sua dimensione (`os.path.getsize`) e sommala a un accumulatore per calcolare la dimensione totale della directory. Se la dimensione totale è maggiore o uguale alla soglia indicata da `--threshold`, apri in modalità append il file di log `dir-size-monitor.log` nella directory specificata con `--log` (`open`) e scrivi una riga contenente data e ora corrente (`datetime.now`), uno spazio e la dimensione totale in byte. Lo script deve ripetere questa procedura periodicamente, attendendo un numero di secondi pari al valore indicato da `--interval` tra ciascun controllo (`time.sleep`).

Ad esempio, eseguendo:

```shell
$ python ~/dir-size-monitor/app.py \
    --target ~/documents \
    --threshold 1000 \
    --interval 60 \
    --log ~
```

lo script calcolerà la dimensione totale di tutti i file presenti in `~/documents` (e in tutte le sue sottodirectory) e, se tale dimensione è maggiore o uguale a `1000` byte, scriverà in append in `~/dir-size-monitor.log` la data, l'ora e la dimensione totale. Lo script ripeterà l'operazione ogni `60` secondi.

### 1.2. Service

Crea un'unità service denominata `dir-size-monitor.service` nella tua istanza utente di `systemd`. L'unità deve avviare `~/dir-size-monitor/app.py` con gli argomenti `--target %h/documents`, `--threshold 1000`, `--interval 60`, e `--log %h`, partire all'avvio del sistema e ripartire in caso di fallimenti. Usa questo template:

```
# nome e cognome:
# matricola:
#
# path:
#
# comando per abilitare il service:
# comando per avviare il service:
```

## 2. Filtraggio dei pacchetti e NAT

Configura un firewall Linux usando `iptables`. Il firewall dispone di due interfacce:

| NIC    | Indirizzo di rete  | IP del firewall | Ambito   |
| ------ | ------------------ | --------------- | -------- |
| `eth0` | `203.0.113.0/24`   | `203.0.113.1`   | Pubblico |
| `eth1` | `10.20.30.0/24`    | `10.20.30.1`    | Privato  |

Gli host sulla rete `10.20.30.0/24` utilizzano questo firewall come gateway di default. L'host `10.20.30.100` esegue un server web che supporta HTTP sulla porta `8080` e HTTPS sulla porta `8443`.

Applica le seguenti regole:

| Tabella      | Catena          | Regola                                                                                                                                           |
| ------------ | --------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| `filter,nat` | `*`             | Elimina le regole esistenti                                                                                                                      |
| `filter`     | `INPUT,FORWARD` | Scarta tutto a meno che non sia esplicitamente permesso                                                                                          |
| `filter`     | `INPUT`         | Consenti pacchetti ICMP ricevuti su `eth1`                                                                                                       |
| `filter`     | `INPUT`         | Consenti pacchetti SSH (`tcp/22`) ricevuti su `eth1`                                                                                             |
| `filter`     | `FORWARD`       | Consenti pacchetti HTTP (`tcp/80`) e HTTPS (`tcp/443`) ricevuti su `eth0` e `eth1`                                                               |
| `filter`     | `FORWARD`       | Consenti pacchetti con stato `ESTABLISHED,RELATED`                                                                                               |
| `nat`        | `POSTROUTING`   | MASQUERADE pacchetti in uscita da `eth0` affinché gli host privati ricevano risposte da Internet                                                 |
| `nat`        | `PREROUTING`    | DNAT per i pacchetti HTTP (`tcp/80`) ricevuti su `eth0`, inoltrandoli a `10.20.30.100:8080` e assicurandoti che possano raggiungere quell'host   |
| `nat`        | `PREROUTING`    | DNAT per i pacchetti HTTPS (`tcp/443`) ricevuti su `eth0`, inoltrandoli a `10.20.30.100:8443` e assicurandoti che possano raggiungere quell'host |

Usa questo template:

```
# nome e cognome:
# matricola:
```

## 3. Domande a risposta aperta

1. Chi può modificare i bit dei permessi di un file, quale comando può usare e come si invoca tale comando?
2. Che cos'è l'IP spoofing e quali difese possono essere utilizzate contro di esso?
3. Che cos'è un certificato digitale, qual è il suo scopo e come viene tipicamente ottenuto?

Usa questo template:

```
# nome e cognome:
# matricola:

1.

2.

3.
```

---

# February 9, 2026

Exam duration: 2 hours and 30 minutes.

| Section                       | Points |
| ----------------------------- | ------ |
| Daemon (§1)                   | 16     |
| - Python script (§1.1)        | 10/16  |
| - Service (§1.2)              | 6/16   |
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

## 1. Daemon

### 1.1. Python script

Write a Python script that periodically calculates the total size of all files in a specified directory (including all its subdirectories) and logs the date, time, and total size when it exceeds a given threshold expressed in bytes. In your home directory, create the directory `dir-size-monitor` and, inside it, the file `app.py`, using this template:

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

The script must accept exactly four mandatory command-line arguments, parsed with the `argparse` module: `--target`, which specifies the absolute path of the directory to monitor; `--threshold`, which specifies the threshold in bytes (positive integer) above which a warning must be logged; `--interval`, which defines the interval in seconds (positive integer) between each check; and `--log`, which specifies the absolute path of the directory where to save the log file. The name of the log file is always `dir-size-monitor.log`.

After parsing, validate the received inputs: verify that the path specified with `--target` is absolute (`os.path.isabs`), that it exists (`os.path.exists`), and that it is a directory (`os.path.isdir`); also check that the values provided for `--threshold` and `--interval` are positive integers; verify that the path indicated with `--log` exists, that is a directory, and that is absolute. If any check fails, print an explanatory error message to standard error (`print`) and exit with a non-zero status code (`sys.exit`).

After validation, recursively traverse the directory tree at the path provided with `--target` (`os.listdir`, `os.path.join`, `os.path.isdir`). For each file encountered (`os.path.isfile`), get its size (`os.path.getsize`) and add it to an accumulator to calculate the total size of the directory. If the total size is greater than or equal to the threshold indicated by `--threshold`, open in append mode the log file `dir-size-monitor.log` in the directory specified with `--log` (`open`) and write a line containing the current date and time (`datetime.now`), a space, and the total size in bytes. The script must repeat this procedure periodically, waiting for a number of seconds equal to the value indicated by `--interval` between each check (`time.sleep`).

For example, running:

```shell
$ python ~/dir-size-monitor/app.py \
    --target ~/documents \
    --threshold 1000 \
    --interval 60 \
    --log ~
```

the script will calculate the total size of all files in `~/documents` (and in all its subdirectories) and, if that size is greater than or equal to `1000` bytes, will append to `~/dir-size-monitor.log` the date, time, and total size. The script will repeat the operation every `60` seconds.

### 1.2. Service

Create a service unit named `dir-size-monitor.service` in your user instance of `systemd`. The unit must start `~/dir-size-monitor/app.py` with the arguments `--target %h/documents`, `--threshold 1000`, `--interval 60`, and `--log %h`, start at system boot, and restart in case of failures. Use this template:

```
# first and last name:
# student id:
#
# path:
#
# command to enable the service:
# command to start the service:
```

## 2. Packet filtering and NAT

Configure a Linux firewall using `iptables`. The firewall has two interfaces:

| NIC    | Network address  | Firewall IP   | Scope   |
| ------ | ---------------- | ------------- | ------- |
| `eth0` | `203.0.113.0/24` | `203.0.113.1` | Public  |
| `eth1` | `10.20.30.0/24`  | `10.20.30.1`  | Private |

Hosts on the `10.20.30.0/24` network use this firewall as their default gateway. Host `10.20.30.100` runs a web server that supports HTTP on port `8080` and HTTPS on port `8443`.

Apply the following rules:

| Table        | Chain           | Rule                                                                                                                                     |
| ------------ | --------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| `filter,nat` | `*`             | Flush all existing rules                                                                                                                 |
| `filter`     | `INPUT,FORWARD` | Drop everything unless explicitly allowed                                                                                                |
| `filter`     | `INPUT`         | Allow ICMP packets received on `eth1`                                                                                                    |
| `filter`     | `INPUT`         | Allow SSH packets (`tcp/22`) received on `eth1`                                                                                          |
| `filter`     | `FORWARD`       | Allow HTTP (`tcp/80`) and HTTPS (`tcp/443`) packets received on `eth0` and `eth1`                                                        |
| `filter`     | `FORWARD`       | Allow packets with state `ESTABLISHED,RELATED`                                                                                           |
| `nat`        | `POSTROUTING`   | MASQUERADE packets leaving via `eth0` so that private hosts receive responses from the Internet                                          |
| `nat`        | `PREROUTING`    | DNAT for HTTP packets (`tcp/80`) received on `eth0`, forwarding them to `10.20.30.100:8080` and ensuring they can reach that host        |
| `nat`        | `PREROUTING`    | DNAT for HTTPS packets (`tcp/443`) received on `eth0`, forwarding them to `10.20.30.100:8443` and ensuring they can reach that host      |

Use this template:

```
# first and last name:
# student id:
```

## 3. Open-ended questions

1. Who may change a file's permission bits, which command can they use, and how is that command invoked?
2. What is IP spoofing, and what defences can be used against it?
3. What is a digital certificate, what purpose does it serve, and how is it typically obtained?

Use this template:

```
# first and last name:
# student id:

1.

2.

3.
```
