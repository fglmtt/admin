# 11 luglio 2025

Durata esame: 2 ore e 30 minuti

| Sezione                             | Punti |
| ----------------------------------- | ----- |
| Processo periodico (§1)             | 16    |
| - Script Python (§1.1)              | 8/16  |
| - Service (§1.2)                    | 4/16  |
| - Timer (§1.3)                      | 4/16  |
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

## 1. Processo periodico

### 1.1. Script Python

Scrivi uno script Python che monitora l’utilizzo percentuale dello spazio disco di una partizione specificata. Quando l’utilizzo percentuale della partizione supera o eguaglia una certa soglia, lo script deve registrare nel file di log la data e l’ora correnti e la percentuale di spazio occupato. Nella tua home directory, crea la directory `disk-usage-monitor` e, al suo interno, il file `app.py`, utilizzando questo template:

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

Lo script deve accettare esattamente due argomenti obbligatori da riga di comando, analizzati con il modulo `argparse`: `--partition`, che indica il percorso assoluto della partizione da monitorare; `--threshold`, che specifica la soglia in percentuale (%) oltre la quale deve essere segnalato l'utilizzo.

Dopo il parsing, valida gli input ricevuti: verifica che il percorso specificato con `--partition` sia assoluto (`os.path.isabs`) e che esista (`os.path.exists`); controlla inoltre che il valore fornito per `--threshold` sia un intero compreso tra 0 e 100. Se un controllo fallisce, stampa un messaggio di errore esplicativo sullo standard error (`print`) ed esci con un codice di stato diverso da zero (`sys.exit`).

Dopo la validazione, calcola l’utilizzo percentuale della partizione indicata (`shutil.disk_usage`); se la percentuale supera o eguaglia la soglia, apri in modalità append il file di log `~/disk-usage-monitor/disk-usage-monitor.log` (`open`), crea la directory se necessario (`os.makedirs`) e scrivi una riga contenente data e ora corrente (`datetime.now`), uno spazio e la percentuale di spazio disco utilizzato.

Ad esempio, eseguendo

```shell
$ python ~/disk-usage-monitor/app.py --partition / --threshold 80
```

lo script controllerà l'utilizzo percentuale della partizione `/`, registrando nel file di log `~/disk-usage-monitor/disk-usage-monitor.log` data, ora e percentuale di spazio usato se questa è uguale o superiore a `80`%.

### 1.2. Service

Crea un'unità service denominata `disk-usage-monitor.service` nella tua istanza utente di `systemd`. L'unità deve avviare `~/disk-usage-monitor/app.py` con gli argomenti `--partition /` e `--threshold 90`. Usa questo template:

```
# nome e cognome:
# matricola:
#
# path:
```

### 1.3. Timer

Crea un'unità timer denominata `disk-usage-monitor.timer` nella tua istanza utente di `systemd`. Configurala per avviare `disk-usage-monitor.service` ogni 2 minuti. Usa questo template:

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

Configura un firewall Linux utilizzando `iptables`. Il firewall ha due interfacce:

| NIC    | Indirizzo di rete | IP del firewall | Ambito   |
| ------ | ----------------- | --------------- | -------- |
| `eth0` | `203.0.113.0/24`  | `203.0.113.10`  | Pubblico |
| `eth1` | `192.168.30.0/24` | `192.168.30.1`  | Privato  |

Gli host della rete `192.168.30.0/24` utilizzano il firewall come gateway predefinito. L’host `192.168.30.60` esegue un server HTTP sulla porta `8080`.

Applica le seguenti regole:

| Tabella      | Catena          | Regola                                                                                                                                                |
| ------------ | --------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| `filter,nat` | `*`             | Elimina tutte le regole esistenti                                                                                                                     |
| `filter`     | `INPUT,FORWARD` | Scarta tutto a meno che non sia esplicitamente permesso                                                                                               |
| `filter`     | `INPUT`         | Consenti pacchetti ICMP ricevuti su `eth0` e `eth1`                                                                                                   |
| `filter`     | `INPUT`         | Consenti pacchetti SSH (`tcp/22`) ricevuti su `eth1` e provenienti esclusivamente dall’host amministrativo `192.168.30.200`                           |
| `filter`     | `FORWARD`       | Consenti tutti i pacchetti ricevuti su `eth1` e in uscita su `eth0`                                                                                   |
| `filter`     | `FORWARD`       | Consenti pacchetti con stato `ESTABLISHED,RELATED`                                                                                                    |
| `nat`        | `POSTROUTING`   | MASQUERADE pacchetti in uscita da `eth0` affinché gli host privati ricevano risposte da Internet                                                      |
| `nat`        | `PREROUTING`    | Applica DNAT ai pacchetti HTTP (`tcp/80`) ricevuti su `eth0`, inoltrandoli a `192.168.30.60:8080` e assicurandoti che possano raggiungere quell'host  |

Usa questo template:

```
# nome e cognome:
# matricola:
```

## 3. Domande a risposta aperta

1. Che cos'è l'esecuzione set-UID, perché `passwd` ne ha bisogno e cosa succede quando un utente normale esegue `passwd`?
2. Che cos'è l'ARP spoofing, quali debolezze del protocollo ARP sfrutta e come si svolge in pratica un attacco MITM?
3. Che cos'è la crittografia a chiave pubblica, come funziona e quali sono i suoi principali vantaggi e svantaggi?

Usa questo template:

```
# nome e cognome:
# matricola:

1.

2.

3.
```

# July 11, 2025

Exam duration: 2 hours and 30 minutes

| Section                       | Points |
| ----------------------------- | ------ |
| Periodic process (§1)         | 16     |
| - Python script (§1.1)        | 8/16   |
| - Service (§1.2)              | 4/16   |
| - Timer (§1.3)                | 4/16   |
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

## 1. Periodic process

### 1.1. Python script

Write a Python script that monitors the percentage usage of disk space on a specified partition. When the partition's usage percentage exceeds or equals a given threshold, the script must record in a log file the current date and time and the percentage of space used. In your home directory, create the directory `disk-usage-monitor` and, inside it, the file `app.py`, using this template:

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

The script must accept exactly two required command-line arguments, parsed with the `argparse` module: `--partition`, which specifies the absolute path of the partition to monitor; and `--threshold`, which specifies the percentage (%) threshold above which usage must be reported.

After parsing, validate the inputs: check that the path given with `--partition` is absolute (`os.path.isabs`) and exists (`os.path.exists`); also ensure that the value provided for `--threshold` is an integer between 0 and 100. If any check fails, print an explanatory error message to standard error (`print`) and exit with a non-zero status code (`sys.exit`).

After validation, calculate the partition's usage percentage (`shutil.disk_usage`); if the percentage exceeds or equals the threshold, open in append mode the log file `~/disk-usage-monitor/disk-usage-monitor.log` (`open`), create that directory if necessary (`os.makedirs`), and write a line containing the current date and time (`datetime.now`), a space, and the percentage of disk space used.

For example, running

```shell
$ python ~/disk-usage-monitor/app.py --partition / --threshold 80
```

the script will check the usage percentage of the `/` partition, recording in the log file `~/disk-usage-monitor/disk-usage-monitor.log` the date, time, and used space percentage if it is equal to or above `80`%.

### 1.2. Service

Create a service unit named `disk-usage-monitor.service` in your user instance of `systemd`. The unit must launch `~/disk-usage-monitor/app.py` with the arguments `--partition /` and `--threshold 90`. Use this template:

```
# first and last name:
# student id:
#
# path:
```

### 1.3. Timer

Create a timer unit named `disk-usage-monitor.timer` in your user instance of `systemd`. Configure it to start `disk-usage-monitor.service` every 2 minutes. Use this template:

```
# first and last name:
# student id:
#
# command to enable the timer:
# command to start the timer:
```

## 2. Packet filtering and NAT

Configure a Linux firewall using `iptables`. The firewall has two interfaces:

|NIC|Network Address|Firewall IP|Scope|
|---|---|---|---|
|`eth0`|`203.0.113.0/24`|`203.0.113.10`|Public|
|`eth1`|`192.168.30.0/24`|`192.168.30.1`|Private|

Hosts on the `192.168.30.0/24` network use the firewall as their default gateway. Host `192.168.30.60` runs an HTTP server on port `8080`.

Apply the following rules:

| Table        | Chain           | Rule                                                                                                                                    |
| ------------ | --------------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| `filter,nat` | `*`             | Delete all existing rules                                                                                                               |
| `filter`     | `INPUT,FORWARD` | Drop everything unless explicitly allowed                                                                                               |
| `filter`     | `INPUT`         | Allow ICMP packets received on `eth0` and `eth1`                                                                                        |
| `filter`     | `INPUT`         | Allow SSH (`tcp/22`) packets received on `eth1` and originating exclusively from the administrative host `192.168.30.200`               |
| `filter`     | `FORWARD`       | Allow all packets received on `eth1` and outgoing on `eth0`                                                                             |
| `filter`     | `FORWARD`       | Allow packets in the `ESTABLISHED,RELATED` state                                                                                        |
| `nat`        | `POSTROUTING`   | MASQUERADE packets leaving via `eth0` so that private hosts receive responses from the Internet                                         |
| `nat`        | `PREROUTING`    | Apply DNAT to HTTP (`tcp/80`) packets received on `eth0`, forwarding them to `192.168.30.60:8080` and ensuring they can reach that host |

Use this template:

```
# first and last name:
# student id:
```

## 3. Open-ended questions

1. What is set-UID execution, why does `passwd` need it, and what happens when a regular user runs `passwd`?
2. What is ARP spoofing, which weaknesses in the ARP protocol does it exploit, and how does a MITM attack unfold in practice?
3. What is public key cryptography, how does it work, and what are its primary advantages and disadvantages?

Use this template:

```
# first and last name:
# student id:

1.

2.

3.
```
