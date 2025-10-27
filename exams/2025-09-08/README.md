# 8 settembre 2025

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

Scrivi uno script Python che analizza i file di log in una directory specificata e nelle sue sottodirectory, estraendo le righe che contengono una stringa specificata e scrivendole in file di output nella directory di backup denominata `backup`, creata (se necessario) in `~`. Nella tua home directory, crea una directory chiamata `log-extractor` e, al suo interno, un file chiamato `app.py`, utilizzando questo template:

```python
# nome e cognome:
# matricola:
#
# path: 

import argparse
import os
import sys

def main():
    pass


if __name__ == "__main__":
    main()
```

Lo script deve accettare esattamente due argomenti da linea di comando, analizzati con il modulo `argparse`. Il primo argomento, `--path`, è una stringa obbligatoria che specifica il percorso assoluto della directory da analizzare. Il secondo argomento, `--pattern`, è una stringa obbligatoria che specifica il pattern da cercare all'interno dei file di log, ovvero quei file che hanno estensione `.log`.

Dopo il parsing, valida entrambi gli input: controlla che il percorso sia assoluto (`os.path.isabs`), esista (`os.path.exists`) e sia una directory (`os.path.isdir`); verifica che `--pattern` sia una stringa non vuota. Se un controllo fallisce, stampa un messaggio di errore esplicativo sullo standard error (`print`) ed esci con un codice di stato diverso da zero (`sys.exit`).

Dopo la validazione, assicurati che la directory `backup` esista in `~` (`os.path.expanduser`, `os.makedirs`). Percorri ricorsivamente l'albero delle directory al percorso fornito (`os.listdir`, `os.path.join`, `os.path.isdir`). Per ogni file di log incontrato (`os.path.isfile`, `str.endswith`), verifica se contiene il pattern specificato leggendone il contenuto (`open`). Se il pattern viene trovato, estrai le righe corrispondenti e scrivile in un file con lo stesso nome nella directory `~/backup` (`open`, `file.writelines`), stampando un messaggio di log sullo standard output (`print`) che indica il numero di righe scritte e il nome del file di destinazione.

Ad esempio, eseguendo:

```shell
$ python ~/log-extractor/app.py \
    --path ~/logs \
    --pattern ERROR   
```

lo script estrarrà tutte le righe contenenti la stringa `ERROR` dai file con estensione `.log` presenti in `~/logs` e nelle sue sottodirectory, scrivendole in file corrispondenti nella cartella `~/backup`.

### 1.2. Service

Crea un'unità service denominata `log-extractor.service` nella tua istanza utente di `systemd`. Configurala per eseguire `~/log-extractor/app.py` con gli argomenti `--path %h/logs` e `--pattern ERROR`. Usa questo template:

```
# nome e cognome:
# matricola:
#
# path: 
```

### 1.3. Timer

Crea un'unità timer denominata `log-extractor.timer` nella tua istanza utente di `systemd`. Configurala per attivare `log-extractor.service` ogni lunedì e venerdì alle 02:00. Usa questo template:

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

Configura un firewall Linux usando `iptables`. Il firewall dispone di due interfacce:

| NIC    | Indirizzo di rete | IP del firewall | Ambito   |
| ------ | ----------------- | --------------- | -------- |
| `eth0` | `198.51.100.0/24` | `198.51.100.5`  | Pubblico |
| `eth1` | `172.16.10.0/24`  | `172.16.10.1`   | Privato  |

Gli host sulla rete `172.16.10.0/24` utilizzano questo firewall come gateway di default. L'host `172.16.10.30` esegue un server DNS (`udp/53`) e un server HTTP (`tcp/8080`).

Applica le seguenti regole:

| Tabella      | Catena          | Regola                                                                                                                                         |
| ------------ | --------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| `filter,nat` | `*`             | Elimina le regole esistenti                                                                                                                    |
| `filter`     | `INPUT,FORWARD` | Scarta tutto a meno che non sia esplicitamente permesso                                                                                        |
| `filter`     | `INPUT`         | Consenti pacchetti ICMP ricevuti su `eth1`                                                                                                     |
| `filter`     | `INPUT`         | Consenti pacchetti SSH (`tcp/22`) ricevuti su `eth1`                                                                                           |
| `filter`     | `FORWARD`       | Consenti pacchetti DNS (`udp/53`) ricevuti su `eth1` destinati a `172.16.10.30`                                                                |
| `filter`     | `FORWARD`       | Consenti tutti i pacchetti ricevuti su `eth1` e in uscita su `eth0`                                                                            |
| `filter`     | `FORWARD`       | Consenti pacchetti con stato `ESTABLISHED,RELATED`                                                                                             |
| `nat`        | `POSTROUTING`   | SNAT per i pacchetti in uscita su `eth0` affinché gli host privati ricevano risposte da Internet                                               |
| `nat`        | `PREROUTING`    | DNAT per i pacchetti HTTP (`tcp/80`) ricevuti su `eth0`, inoltrandoli a `172.16.10.30:8080` e assicurandoti che possano raggiungere quell'host |

Usa questo template:

```
# nome e cognome:
# matricola:
```

## 3. Domande a risposta aperta

1. Qual è la funzione dei bit set-UID, set-GID e sticky, a quali file regolari o directory si applicano e come influenzano i relativi permessi?
2. Cos'è l'ingegneria sociale, perché è particolarmente difficile da contrastare e qual è una forma comune di questo tipo di attacco?
3. Che cos'è la crittografia a chiave simmetrica, come funziona e quali sono i suoi principali vantaggi e svantaggi?

Usa questo template:

```
# nome e cognome:
# matricola:

1.

2.

3.
```

---

# September 8, 2025

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

Write a Python script that analyzes log files in a specified directory and its subdirectories, extracting lines that contain a specified string and writing them to output files in a backup directory named `backup`, created (if necessary) in `~`. In your home directory, create a directory called `log-extractor` and, within it, a file named `app.py`, using this template:

```python
# first and last name:
# student id:
#
# path: 

import argparse
import os
import sys

def main():
    pass


if __name__ == "__main__":
    main()
```

The script must accept exactly two command-line arguments, parsed using the `argparse` module. The first argument, `--path`, is a mandatory string specifying the absolute path of the directory to analyze. The second argument, `--pattern`, is a mandatory string specifying the pattern to search for within log files, i.e., those files with a `.log` extension.

After parsing, validate both inputs: check that the path is absolute (`os.path.isabs`), exists (`os.path.exists`), and is a directory (`os.path.isdir`); verify that `--pattern` is a non-empty string. If any check fails, print an explanatory error message to standard error (`print`) and exit with a non-zero status code (`sys.exit`).

After validation, ensure the `backup` directory exists in `~` (`os.path.expanduser`, `os.makedirs`). Recursively traverse the directory tree at the provided path (`os.listdir`, `os.path.join`, `os.path.isdir`). For each log file encountered (`os.path.isfile`, `str.endswith`), check if it contains the specified pattern by reading its content (`open`). If the pattern is found, extract the corresponding lines and write them to a file with the same name in the `~/backup` directory (`open`, `file.writelines`), printing a log message to standard output (`print`) indicating the number of lines written and the destination file name.

For example, running:

```shell
$ python ~/log-extractor/app.py \
    --path ~/logs \
    --pattern ERROR   
```

the script will extract all lines containing the string `ERROR` from files with a `.log` extension in `~/logs` and its subdirectories, writing them to corresponding files in the `~/backup` folder.

### 1.2. Service

Create a service unit named `log-extractor.service` in your user instance of `systemd`. Configure it to run `~/log-extractor/app.py` with the arguments `--path %h/logs` and `--pattern ERROR`. Use this template:

```
# first and last name:
# student id:
#
# path: 
```

### 1.3. Timer

Create a timer unit named `log-extractor.timer` in your user instance of `systemd`. Configure it to activate `log-extractor.service` every Monday and Friday at 02:00. Use this template:

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

| NIC    | Network Address   | Firewall IP     | Scope    |
| ------ | ----------------- | --------------- | -------- |
| `eth0` | `198.51.100.0/24` | `198.51.100.5`  | Public   |
| `eth1` | `172.16.10.0/24`  | `172.16.10.1`   | Private  |

Hosts on the `172.16.10.0/24` network use this firewall as the default gateway. The host `172.16.10.30` runs a DNS server (`upd/53`) and an HTTP server (`tcp/8080`).

Apply the following rules:

| Table        | Chain           | Rule                                                                                                                                           |
| ------------ | --------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| `filter,nat` | `*`             | Clear existing rules                                                                                                                           |
| `filter`     | `INPUT,FORWARD` | Drop everything unless explicitly allowed                                                                                                      |
| `filter`     | `INPUT`         | Allow ICMP packets received on `eth1`                                                                                                          |
| `filter`     | `INPUT`         | Allow SSH packets (`tcp/22`) received on `eth1`                                                                                                |
| `filter`     | `FORWARD`       | Allow DNS packets (`udp/53`) received on `eth1` destined for `172.16.10.30`                                                                    |
| `filter`     | `FORWARD`       | Allow all packets received on `eth1` and outgoing on `eth0`                                                                                    |
| `filter`     | `FORWARD`       | Allow packets with state `ESTABLISHED,RELATED`                                                                                                 |
| `nat`        | `POSTROUTING`   | SNAT for packets outgoing on `eth0` so private hosts receive responses from the Internet                                                       |
| `nat`        | `PREROUTING`    | DNAT for HTTP packets (`tcp/80`) received on `eth0`, forwarding them to `172.16.10.30:8080` and ensuring they can reach that host               |

Use this template:

```
# first and last name:
# student id:
```

## 3. Open-ended questions

1. What are the purposes of the set-UID, set-GID, and sticky bits, to which regular files or directories does each apply, and how do they alter permission checks?
2. What is social engineering, why is it particularly difficult to defend against, and what is one common form of this attack?
3. What is symmetric key cryptography, how does it work, and what are its primary advantages and disadvantages?

Use this template:

```
# first and last name:
# student id:

1.

2.

3.
```
