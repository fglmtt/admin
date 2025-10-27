# 3 novembre 2025

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

Scrivi uno script Python che periodicamente analizza una directory specificata (incluse tutte le sue sottodirectory) per rimuovere i file la cui data di ultima modifica è antecedente a una certa soglia espressa in giorni. Nella tua home directory, crea la directory `old-file-detector` e, al suo interno, il file `app.py`, utilizzando questo template:

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

Lo script deve accettare esattamente quattro argomenti obbligatori da linea di comando, analizzati con il modulo `argparse`: `--target`, che indica il percorso assoluto della directory da controllare; `--days`, che specifica il numero di giorni (intero positivo) oltre i quali un file è considerato "vecchio"; `--interval`, che definisce l'intervallo in secondi (intero positivo) tra ogni controllo; e `--log`, che indica dove salvare il file di log. Il nome del file di log è sempre `old-file-detector.log`.

Dopo il parsing, valida gli input ricevuti: verifica che il percorso specificato con `--target` sia assoluto (`os.path.isabs`), che esista (`os.path.exists`) e che sia una directory (`os.path.isdir`); controlla inoltre che i valori forniti per `--days` e `--interval` siano interi positivi; verifica che il percorso indicato con `--log` esista (`os.path.exists`) e sia una directory (`os.path.isdir`).

Dopo la validazione, percorri quindi ricorsivamente l'albero delle directory al percorso fornito con `--target` (`os.listdir`, `os.path.join`, `os.path.isdir`). Per ogni file (`os.path.isfile`), ottieni la data di ultima modifica (`os.path.getmtime`) e confrontala con la soglia temporale corrispondente a `--days` (calcolando tale soglia come `time.time() - days * 86400`). Se la data di ultima modifica è antecedente alla soglia, scrivi il percorso assoluto del file in `old-file-detector.log` (`open`) e rimuovi tale file (`os.remove`). Ogni operazione di scrittura nel file di log deve essere fatta in modalità append. Lo script deve ripetere questa procedura periodicamente, attendendo un numero di secondi pari al valore indicato da `--interval` tra ciascun controllo (`time.sleep`).

Ad esempio, eseguendo:

```shell
$ python ~/old-file-detector/app.py \
    --target ~/archive \
    --days 30 \
    --interval 60 \
    --log ~
```

lo script dovrà individuare tutti i file modificati per l'ultima volta 30 o più giorni fa presenti in `~/archive` (e in tutte le sue sottodirectory), scrivere in append in `~/old-file-detector.log` il percorso di ciascuno dei file individuati e rimuovere tali file. Lo script ripeterà l'operazione ogni `60` secondi.

> [!tip]
> Per testare lo script puoi creare manualmente alcuni file nella directory `~/archive` e retrodatare la loro data di ultima modifica con il comando:
> 
> ```
> $ touch -d "45 days ago" <path>
> ```

### 1.2. Service

Crea un'unità service denominata `old-file-detector.service` nella tua istanza utente di `systemd`. L'unità deve avviare `~/old-file-detector/app.py` con gli argomenti `--target %h/archive`, `--days 30`, `--interval 60`, e `--log %h`, partire all'avvio del sistema e ripartire in caso di fallimenti. Usa questo template:

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

| NIC    | Indirizzo di rete | IP del firewall | Ambito   |
| ------ | ----------------- | --------------- | -------- |
| `eth0` | `203.0.113.0/24`  | `203.0.113.10`  | Pubblico |
| `eth1` | `10.0.0.0/24`     | `10.0.0.1`      | Privato  |

Gli host sulla rete `10.0.0.0/24` utilizzano questo firewall come gateway di default. L'host `10.0.0.50` esegue un server SSH (`tcp/22`) e un server HTTPS (`tcp/8443`).

Applica le seguenti regole:

| Tabella      | Catena          | Regola                                                                                                                                        |
| ------------ | --------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| `filter,nat` | `*`             | Elimina le regole esistenti                                                                                                                   |
| `filter`     | `INPUT,FORWARD` | Scarta tutto a meno che non sia esplicitamente permesso                                                                                       |
| `filter`     | `INPUT`         | Consenti pacchetti ICMP ricevuti su `eth1`                                                                                                    |
| `filter`     | `INPUT`         | Consenti pacchetti SSH (`tcp/22`) ricevuti su `eth1` e provenienti esclusivamente dall'host amministrativo `10.0.0.100`                       |
| `filter`     | `FORWARD`       | Consenti tutti i pacchetti ricevuti su `eth1` e in uscita su `eth0`                                                                           |
| `filter`     | `FORWARD`       | Consenti pacchetti con stato `ESTABLISHED,RELATED`                                                                                            |
| `nat`        | `POSTROUTING`   | SNAT per i pacchetti in uscita su `eth0` affinché gli host privati ricevano risposte da Internet                                              |
| `nat`        | `PREROUTING`    | DNAT per i pacchetti HTTPS (`tcp/443`) ricevuti su `eth0`, inoltrandoli a `10.0.0.50:8443` e assicurandoti che possano raggiungere quell'host |

Usa questo template:

```
# nome e cognome:
# matricola:
```

## 3. Domande a risposta aperta

1. Perché `sudo` è generalmente preferito al login diretto come `root` o all'uso di `su` per ottenere i privilegi di `root`, e quali sono i suoi principali vantaggi e svantaggi?
2. Che cos'è l'IPv4 source routing e in che modo un attaccante può sfruttarlo?
3. Che cos'è una digital signature, qual è il suo scopo e come può essere creata utilizzando la crittografia a chiave pubblica?

Usa questo template:

```
# nome e cognome:
# matricola:

1.

2.

3.
```

# November 3, 2025

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

Write a Python script that periodically scans a specified directory (including all its subdirectories) to remove files whose last modification date is earlier than a given threshold expressed in days. In your home directory, create the directory `old-file-detector` and, inside it, the file `app.py`, using this template:

```python
# first and last name:
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

The script must accept exactly four mandatory command-line arguments, parsed with the `argparse` module: `--target`, which specifies the absolute path of the directory to check; `--days`, which specifies the number of days (positive integer) after which a file is considered "old"; `--interval`, which defines the interval in seconds (positive integer) between each check; and `--log`, which specifies where to save the log file. The name of the log file is always `old-file-detector.log`.

After parsing, validate the received inputs: verify that the path specified with `--target` is absolute (`os.path.isabs`), that it exists (`os.path.exists`), and that it is a directory (`os.path.isdir`); also check that the values provided for `--days` and `--interval` are positive integers; verify that the path indicated with `--log` exists (`os.path.exists`) and is a directory (`os.path.isdir`).

After validation, recursively traverse the directory tree at the path provided with `--target` (`os.listdir`, `os.path.join`, `os.path.isdir`). For each file (`os.path.isfile`), obtain its last modification date (`os.path.getmtime`) and compare it with the time threshold corresponding to `--days` (calculating this threshold as `time.time() - days * 86400`). If the last modification date is earlier than the threshold, write the absolute path of the file to `old-file-detector.log` (`open`) and remove that file (`os.remove`). Each write operation to the log file must be done in append mode. The script must repeat this procedure periodically, waiting for a number of seconds equal to the value indicated by `--interval` between each check (`time.sleep`).

For example, running:

```shell
$ python ~/old-file-detector/app.py \
    --target ~/archive \
    --days 30 \
    --interval 60 \
    --log ~
```

the script will identify all files last modified 30 or more days ago in `~/archive` (and in all its subdirectories), append the path of each identified file to `~/old-file-detector.log`, and remove those files. The script will repeat the operation every `60` seconds.

> [!tip]  
> To test the script, you can manually create some files in the `~/archive` directory and backdate their last modification date with the command:
> 
> ```
> $ touch -d "45 days ago" <path>
> ```

### 1.2. Service

Create a service unit named `old-file-detector.service` in your user instance of `systemd`. The unit must start `~/old-file-detector/app.py` with the arguments `--target %h/archive`, `--days 30`, `--interval 60`, and `--log %h`, start at system boot, and restart in case of failures. Use this template:

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

|NIC|Network address|Firewall IP|Scope|
|---|---|---|---|
|`eth0`|`203.0.113.0/24`|`203.0.113.10`|Public|
|`eth1`|`10.0.0.0/24`|`10.0.0.1`|Private|

Hosts on the `10.0.0.0/24` network use this firewall as their default gateway. Host `10.0.0.50` runs an SSH server (`tcp/22`) and an HTTPS server (`tcp/8443`).

Apply the following rules:

| Table        | Chain           | Rule                                                                                                                             |
| ------------ | --------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| `filter,nat` | `*`             | Flush all existing rules                                                                                                         |
| `filter`     | `INPUT,FORWARD` | Drop everything unless explicitly allowed                                                                                        |
| `filter`     | `INPUT`         | Allow ICMP packets received on `eth1`                                                                                            |
| `filter`     | `INPUT`         | Allow SSH packets (`tcp/22`) received on `eth1` and coming exclusively from the administrative host `10.0.0.100`                 |
| `filter`     | `FORWARD`       | Allow all packets received on `eth1` and outgoing on `eth0`                                                                      |
| `filter`     | `FORWARD`       | Allow packets with state `ESTABLISHED,RELATED`                                                                                   |
| `nat`        | `POSTROUTING`   | SNAT for packets going out on `eth0` so that private hosts can receive replies from the Internet                                 |
| `nat`        | `PREROUTING`    | DNAT for HTTPS packets (`tcp/443`) received on `eth0`, forwarding them to `10.0.0.50:8443` and ensuring they can reach that host |

Use this template:

```
# first and last name:
# student id:
```

## 3. Open-ended questions

1. Why is `sudo` generally preferred to direct `root` login or `su` for obtaining `root` privileges, and what are its main advantages and drawbacks?
2. What is IPv4 source routing, and how can an attacker exploit it?
3. What is a digital signature, what is its purpose, and how can it be created using public key cryptography?

Use this template:

```
# first and last name:
# student id:

1.

2.

3.
```
