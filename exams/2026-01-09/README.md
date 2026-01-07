# 9 gennaio 2026

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

Scrivi uno script Python che comprime tutti i file più grandi di una certa dimensione (in byte) da una directory specificata e tutte le sue sottodirectory in un archivio zip nella directory `~/archives`. Nella tua home directory, crea una directory chiamata `file-compressor` e, al suo interno, un file chiamato `app.py`, utilizzando questo template:

```python
# nome e cognome:
# matricola:
#
# path: 

import argparse
import os
import sys
import zipfile
import time

def main():
    pass


if __name__ == "__main__":
    main()
```

Lo script deve accettare esattamente due argomenti da linea di comando, analizzati con il modulo `argparse`. Il primo argomento, `--path`, è una stringa obbligatoria che indica il percorso assoluto della directory da scansionare. Il secondo argomento, `--size`, è un intero obbligatorio che specifica la soglia di dimensione (in byte) oltre la quale i file devono essere compressi.

Dopo il parsing, valida entrambi gli input: verifica che il percorso sia assoluto (`os.path.isabs`), esista (`os.path.exists`) e sia una directory (`os.path.isdir`); verifica anche che `--size` sia un intero positivo. Se uno dei controlli fallisce, stampa un messaggio di errore esplicativo sullo standard error (`print`) ed esci con un codice di stato diverso da zero (`sys.exit`).

Una volta validati, assicurati che esista una cartella chiamata `archives` in `~` (`os.path.expanduser`, `os.makedirs`). Quindi, percorri ricorsivamente l'albero delle directory al percorso fornito come primo argomento (`os.listdir`, `os.path.join`, `os.path.isdir`). Per ogni file incontrato (`os.path.isfile`), controlla la sua dimensione (`os.path.getsize`). Se la dimensione del file è maggiore o uguale alla soglia, crea un nuovo file zip utilizzando il timestamp corrente come nome del file (`time.time` per ottenere il timestamp), aggiungi il file all'archivio e rimuovi il file originale (`os.remove`).

Ecco un frammento di codice che mostra come comprimere un file:

```python
with zipfile.ZipFile('/path/to/archive.zip', 'a') as zipf:
    zipf.write('/path/to/file', arcname='filename')
```

Ad esempio, eseguendo:

```shell
$ python ~/file-compressor/app.py \
    --path ~/media \
    --size 1048576
```

lo script comprimerà in `~/archives/1673038800.zip` (supponendo che quello fosse il timestamp corrente) tutti i file più grandi di 1 MB (1048576 byte) trovati in `~/media` e in tutte le sue sottodirectory, quindi cancellerà i file originali.

### 1.2. Service

Crea un'unità service chiamata `file-compressor.service` nella tua istanza utente di `systemd`. Configurala per avviare `~/file-compressor/app.py` con gli argomenti `--path %h/media` e `--size 1048576`. Usa questo template:

```
# nome e cognome:
# matricola:
#
# path: 
```

### 1.3. Timer

Crea un'unità timer chiamata `file-compressor.timer` nella tua istanza utente di `systemd`. Configurala per attivare `file-compressor.service` alle 02:00 di ogni lunedì e giovedì. Usa questo template:

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
| `eth0` | `192.0.2.0/24`    | `192.0.2.5`     | Pubblico |
| `eth1` | `172.16.0.0/12`   | `172.16.0.1`    | Privato  |

Gli host sulla rete `172.16.0.0/12` utilizzano questo firewall come gateway di default.  L'host `172.16.0.30` esegue un server DNS (`udp/5353`) e un server HTTP (`tcp/8080`).

Applica le seguenti regole:

| Tabella      | Catena          | Regola                                                                                                                                        |
| ------------ | --------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| `filter,nat` | `*`             | Elimina le regole esistenti                                                                                                                   |
| `filter`     | `INPUT,FORWARD` | Scarta tutto a meno che non sia esplicitamente permesso                                                                                       |
| `filter`     | `INPUT`         | Consenti pacchetti SSH (`tcp/22`) ricevuti su `eth1` e provenienti esclusivamente dall'host amministrativo `172.16.0.50`                      |
| `filter`     | `FORWARD`       | Consenti tutti i pacchetti ricevuti su `eth1` e in uscita su `eth0`                                                                           |
| `filter`     | `FORWARD`       | Consenti pacchetti con stato `ESTABLISHED,RELATED`                                                                                            |
| `nat`        | `POSTROUTING`   | SNAT per i pacchetti in uscita su `eth0` affinché gli host privati ricevano risposte da Internet                                              |
| `nat`        | `PREROUTING`    | DNAT per i pacchetti UDP (`udp/53`) ricevuti su `eth0`, inoltrandoli a `172.16.0.30:5353` e assicurandoti che possano raggiungere quell'host  |
| `nat`        | `PREROUTING`    | DNAT per i pacchetti HTTP (`tcp/80`) ricevuti su `eth0`, inoltrandoli a `172.16.0.30:8080` e assicurandoti che possano raggiungere quell'host |

Usa questo template:

```
# nome e cognome:
# matricola:
```

## 3. Domande a risposta aperta

1. Quali operazioni può eseguire solo il proprietario del processo (o `root`), e quali identità sono associate a un processo?
2. Che cos’è l'*insider abuse*, e perché è spesso più difficile da rilevare rispetto agli attacchi esterni?
3. Che cos’è una funzione di hash, e quali proprietà specifiche definiscono una funzione di hash crittografica?

Usa questo template:

```
# nome e cognome:
# matricola:

1.

2.

3.
```

---

# January 9, 2026

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

Write a Python script that compresses all files larger than a certain size (in bytes) from a specified directory and all its subdirectories into a zip archive in `~/archives`. In your home directory, create a directory called `file-compressor` and, inside it, a file called `app.py`, using this template:

```python
# first and last name:
# student id:
#
# path: 

import argparse
import os
import sys
import zipfile
import time

def main():
    pass


if __name__ == "__main__":
    main()
```

The script must accept exactly two command-line arguments, parsed with the `argparse` module. The first argument, `--path`, is a required string indicating the absolute path of the directory to scan. The second argument, `--size`, is a required integer specifying the size threshold (in bytes) above which files should be compressed.

After parsing, validate both inputs: check that the path is absolute (`os.path.isabs`), exists (`os.path.exists`), and is a directory (`os.path.isdir`); also verify that `--size` is a positive integer. If any check fails, print an explanatory error message to standard error (`print`) and exit with a non-zero status code (`sys.exit`).

Once validated, ensure that a folder named `archives` exists in `~` (`os.path.expanduser`, `os.makedirs`). Then recursively traverse the directory tree at the path provided as the first argument (`os.listdir`, `os.path.join`, `os.path.isdir`). For each file encountered (`os.path.isfile`), check its size (`os.path.getsize`). If the file size is greater than or equal to the threshold value, create a new zip file using the current timestamp as its name (`time.time` to get the timestamp), add the file to the archive, and remove the original file (`os.remove`).

Here’s the code snippet that shows how to zip a file:

```python
with zipfile.ZipFile('/path/to/archive.zip', 'a') as zipf:
    zipf.write('/path/to/file', arcname='filename')
```

For example, running

```shell
$ python ~/file-compressor/app.py \
    --path ~/media \
    --size 1048576
```

the script should compress into `~/archives/1673038800.zip` (suppose that was the current timestamp) all files larger than 1 MB (1048576 bytes) found in `~/media` and all its subdirectories, and then delete the original files.

### 1.2. Service

Create a service unit named `file-compressor.service` in your user instance of `systemd`. Configure it to start `~/file-compressor/app.py` with the arguments `--path %h/media` and `--size 1048576`. Use this template:

```
# first and last name:
# student id:
#
# path: 
```

### 1.3. Timer

Create a timer unit named `file-compressor.timer` in your user instance of `systemd`. Configure it to trigger `file-compressor.service` at 02:00 on every Monday and Thursday. Use this template:

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
| `eth0` | `192.0.2.0/24`  | `192.0.2.5`  | Public  |
| `eth1` | `172.16.0.0/12` | `172.16.0.1` | Private |

Hosts on the `172.16.0.0/12` network use this firewall as the default gateway.  
The host `172.16.0.30` runs a DNS server (`udp/5353`) and an HTTP server (`tcp/8080`).

Apply the following rules:

| Table        | Chain           | Rule                                                                                                                             |
| ------------ | --------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| `filter,nat` | `*`             | Clear existing rules                                                                                                             |
| `filter`     | `INPUT,FORWARD` | Drop everything unless explicitly allowed                                                                                        |
| `filter`     | `INPUT`         | Allow SSH packets (`tcp/22`) received on `eth1` and coming exclusively from the administrative host `172.16.0.50`                |
| `filter`     | `FORWARD`       | Allow all packets received on `eth1` and outgoing on `eth0`                                                                      |
| `filter`     | `FORWARD`       | Allow packets with state `ESTABLISHED,RELATED`                                                                                   |
| `nat`        | `POSTROUTING`   | SNAT for packets outgoing on `eth0` so that private hosts receive responses from the Internet                                    |
| `nat`        | `PREROUTING`    | DNAT for UDP packets (`udp/53`) received on `eth0`, forwarding them to `172.16.0.30:5353` and ensuring they can reach that host  |
| `nat`        | `PREROUTING`    | DNAT for HTTP packets (`tcp/80`) received on `eth0`, forwarding them to `172.16.0.30:8080` and ensuring they can reach that host |

Use this template:

```
# first and last name:
# student id:
```

## 3. Open-ended questions

1. Which operations can only the process owner (or `root`) perform, and what identities are associated with a process?
2. What is insider abuse, and why is it often harder to detect than external attacks?
3. What is a hash function, and what specific properties define a cryptographic hash function?

Use this template:

```
# first and last name:
# student id:

1.

2.

3.
```
