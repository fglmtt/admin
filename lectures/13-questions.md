# Questions

## Access control and rootly powers

- What core rules govern the traditional UNIX permission model?
- Which operations can only the file owner (or `root`) perform, and what permission bits can be set on a file?
- Which operations can only the process owner (or `root`) perform, and what identities are associated with a process?
- What is set-UID execution, why does `passwd` need it, and what happens when a regular user runs `passwd`?
- Why is `sudo` generally preferred to direct `root` login or `su` for obtaining `root` privileges, and what are its main advantages and drawbacks?

## The filesystem

- Which file types does UNIX support, and how do the nine permission bits (`rwx` for user, group, and other) govern the allowed operations on each type?
- Why is a lazy unmount (`umount -l`) considered unsafe, which command lets you identify the processes that still hold references to the busy filesystem, and how can you perform a clean unmount instead?
- What are the purposes of the set-UID, set-GID, and sticky bits, to which regular files or directories does each apply, and how do they alter permission checks?
- Who may change a file’s permission bits, which command can they use, and how is that command invoked?
- Who may change a file’s (group) ownership, what rules must be satisfied, and which command performs the operation?

## Networking

- What is ARP spoofing, which weaknesses in the ARP protocol does it exploit, and how does a MITM attack unfold in practice?
- How can an attacker mount a MITM attack with ICMP redirect messages, and which weaknesses in the ICMP protocol make this possible?
- What is IP forwarding, and why is it usually unsafe to leave it enabled on hosts that are not intended to act as routers?
- What is IP spoofing, and what defences can be used against it?
- What is IPv4 source routing, and how can an attacker exploit it?

## Security

- What does the CIA triad stand for in information security, and what does each principle mean?
- What is social engineering, why is it particularly difficult to defend against, and what is one common form of this attack?
- What is a software vulnerability, what is a specific example of such a vulnerability, and how can open-source code review practices help in reducing these vulnerabilities?
- What is the difference between a DoS attack and a DDoS attack, and how do these attacks typically impact the targeted systems?
- What is insider abuse, and why is it often harder to detect than external attacks?
- What is a backup in the context of computer security, and what are the key recommendations for effectively managing backups?
- What are computer viruses and worms, and what are the key differences between these two types of malware?
- What is a rootkit, how does it typically function, and why can it be particularly challenging to detect and remove?
- What are the best practices and recommendations for creating secure passwords, managing passwords effectively, and implementing MFA?
- What is symmetric key cryptography, how does it work, and what are its primary advantages and disadvantages?
- What is public key cryptography, how does it work, and what are its primary advantages and disadvantages?
- What is a digital signature, what is its purpose, and how can it be created using public key cryptography?
- What is a digital certificate, what purpose does it serve, and how is it typically obtained?
- What is a hash function, and what specific properties define a cryptographic hash function?
- What is a firewall, how does a two-stage firewall filtering scheme work, and what role does a DMZ play?