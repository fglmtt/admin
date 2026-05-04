# Packet filtering and NAT

## Table of contents

- [1. Text](#1-text)
- [2. Hints](#2-hints)
    - [2.1. System reference manuals](#21-system-reference-manuals)
    - [2.2. Virtual environment](#22-virtual-environment)
    - [2.3. Default deny](#23-default-deny)
    - [2.4. Packet filtering](#24-packet-filtering)
    - [2.5. NAT](#25-nat)
    - [2.6. Deliverable file](#26-deliverable-file)
- [3. Solution](#3-solution)
- [Licenses](#licenses)

## 1. Text

Configure a Linux firewall using `iptables`. The firewall has two interfaces:

| NIC    | Network address  | Firewall IP   | Scope   |
| ------ | ---------------- | ------------- | ------- |
| `eth0` | `203.0.113.0/24` | `203.0.113.1` | Public  |
| `eth1` | `10.20.30.0/24`  | `10.20.30.1`  | Private |

Hosts on the `10.20.30.0/24` network use this firewall as their default gateway. Host `10.20.30.100` runs a web server that supports Hypertext Transfer Protocol (HTTP) on port `8080` and HTTP Secure (HTTPS) on port `8443`.

Apply the following rules:

| Table        | Chain           | Rule                                                                                                                                |
| ------------ | --------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| `filter,nat` | `*`             | Flush all existing rules                                                                                                            |
| `filter`     | `INPUT,FORWARD` | Drop everything unless explicitly allowed                                                                                           |
| `filter`     | `INPUT`         | Allow ICMP packets received on `eth1`                                                                                               |
| `filter`     | `INPUT`         | Allow SSH packets (`tcp/22`) received on `eth1`                                                                                     |
| `filter`     | `FORWARD`       | Allow HTTP (`tcp/80`) and HTTPS (`tcp/443`) packets received on `eth0` and `eth1`                                                   |
| `filter`     | `FORWARD`       | Allow packets with state `ESTABLISHED,RELATED`                                                                                      |
| `nat`        | `POSTROUTING`   | MASQUERADE packets leaving via `eth0` so that private hosts receive responses from the Internet                                     |
| `nat`        | `PREROUTING`    | DNAT for HTTP packets (`tcp/80`) received on `eth0`, forwarding them to `10.20.30.100:8080` and ensuring they can reach that host   |
| `nat`        | `PREROUTING`    | DNAT for HTTPS packets (`tcp/443`) received on `eth0`, forwarding them to `10.20.30.100:8443` and ensuring they can reach that host |

Use this template:

```
# first and last name:
# student id:
```

## 2. Hints

### 2.1. System reference manuals

`man` displays the system reference manuals. For example, `man:iptables(8)` translates to

```shell
$ man 8 iptables
```

See also `man:iptables-extensions(8)` for the documentation of match modules such as `conntrack` (`--ctstate`).

### 2.2. Virtual environment

The scripts at [`code/up.sh`](https://github.com/fglmtt/admin/blob/main/code/up.sh) and [`code/down.sh`](https://github.com/fglmtt/admin/blob/main/code/down.sh) set up and tear down the topology described in [§1](#1-text) using [`podman`](https://github.com/fglmtt/admin/blob/main/lectures/containers.md#3-podman). Make them executable

```shell
$ chmod +x up.sh down.sh
```

To start the environment

```shell
$ ./up.sh
```

To tear it down

```shell
$ ./down.sh
```

> [!warning]
> A container's [`iptables`](https://github.com/fglmtt/admin/blob/main/lectures/networking.md#11-linux-iptables) rules live in its network namespace and are discarded when the container is removed. Re-running `./up.sh` after `./down.sh` gives you a clean firewall.

Open three shells in separate terminals, one per container

```shell
$ podman exec -it firewall bash
```

```shell
$ podman exec -it client bash
```

```shell
$ podman exec -it web bash
```

Before writing any rule, confirm the topology is wired up correctly. For example, the output below shows which Internet Protocol (IP) address is assigned to which interface on `firewall`:

```shell
ubuntu@firewall:~$ ip a
1: lo: [...]
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
2: eth1@if4: [...]
    link/ether 96:95:c5:05:68:ee brd ff:ff:ff:ff:ff:ff link-netnsid 0
    inet 10.20.30.1/24 brd 10.20.30.255 scope global eth1
       valid_lft forever preferred_lft forever
    inet6 fe80::9495:c5ff:fe05:68ee/64 scope link
       valid_lft forever preferred_lft forever
3: eth0@if6: [...]
    link/ether 3e:56:eb:e1:7c:98 brd ff:ff:ff:ff:ff:ff link-netnsid 0
    inet 203.0.113.1/24 brd 203.0.113.255 scope global eth0
       valid_lft forever preferred_lft forever
    inet6 fe80::3c56:ebff:fee1:7c98/64 scope link
       valid_lft forever preferred_lft forever
```

A host sends all traffic that does not match a more specific route to its default gateway. To check the default gateway on a host

```shell
ubuntu@client:~$ ip r
default via 203.0.113.1 dev eth0
203.0.113.0/24 dev eth0 proto kernel scope link src 203.0.113.50
```

```shell
ubuntu@web:~$ ip r
default via 10.20.30.1 dev eth0
10.20.30.0/24 dev eth0 proto kernel scope link src 10.20.30.100
```

`firewall` is the default gateway both for `web` and `client`. As

```shell
ubuntu@firewall:~$ cat /proc/sys/net/ipv4/ip_forward
1
```

`firewall` has IP forwarding enabled, it will forward packets. Therefore, from `web`, ping `client`

```shell
ubuntu@web:~$ ping 203.0.113.50
PING 203.0.113.50 (203.0.113.50) 56(84) bytes of data.
64 bytes from 203.0.113.50: icmp_seq=1 ttl=63 time=1.15 ms
64 bytes from 203.0.113.50: icmp_seq=2 ttl=63 time=0.235 ms
^C
--- 203.0.113.50 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1006ms
rtt min/avg/max/mdev = 0.235/0.691/1.148/0.456 ms
```

To watch the relay, run `tcpdump` on `firewall`

```shell
ubuntu@firewall:~$ tcpdump -i any icmp
tcpdump: data link type LINUX_SLL2
tcpdump: verbose output suppressed, use -v[v]... for full protocol decode
listening on any, link-type LINUX_SLL2 (Linux cooked v2), snapshot length 262144 bytes
14:00:55.699374 eth0  In  IP 203.0.113.50 > 10.20.30.100: ICMP echo request, id 9, seq 10, length 64
14:00:55.699406 eth1  Out IP 203.0.113.50 > 10.20.30.100: ICMP echo request, id 9, seq 10, length 64
14:00:55.699470 eth1  In  IP 10.20.30.100 > 203.0.113.50: ICMP echo reply, id 9, seq 10, length 64
14:00:55.699478 eth0  Out IP 10.20.30.100 > 203.0.113.50: ICMP echo reply, id 9, seq 10, length 64

[...]
```

- `-i any` tells `tcpdump` to listen on all interfaces at once; you can replace `any` with a specific interface name (e.g., `-i eth0`) to capture traffic on that interface only

> [!note]
> `tcpdump` buffers output before printing it. If you do not see packets immediately, wait a moment.

### 2.3. Default deny

Default deny is two steps — flush every chain in `filter` and `nat` to discard whatever rules existed before, then set the default policy of `INPUT` and `FORWARD` to `DROP`. Leave `OUTPUT` at the default `ACCEPT`: `firewall` is trusted to send replies and any locally-generated traffic. The `nat` table does not filter, so its chain policies stay at the default `ACCEPT`. Therefore

```shell
ubuntu@firewall:~$ iptables -F
ubuntu@firewall:~$ iptables -t nat -F
ubuntu@firewall:~$ iptables -P INPUT DROP
ubuntu@firewall:~$ iptables -P FORWARD DROP
```

To list all rules

```shell
ubuntu@firewall:~$ iptables -L
Chain INPUT (policy DROP)
target     prot opt source               destination

Chain FORWARD (policy DROP)
target     prot opt source               destination

Chain OUTPUT (policy ACCEPT)
target     prot opt source               destination
```

> [!note]
> Like every other `iptables` command, it applies to the specified table. If no table is specified, `filter` is the default. For example, use `iptables -L -t nat` to list all rules of the `nat` table.

> [!warning]
> With these policies in place, any packet not explicitly allowed is dropped. In particular, `web` and `client` can no longer ping `firewall` (`INPUT DROP`), nor can they reach each other (`FORWARD DROP`).

### 2.4. Packet filtering

> [!warning]
> This section uses hypothetical ports to demonstrate `FORWARD` mechanics. This is NOT what required by [§1](#1-text).

Suppose you want `client` to reach `web` on port `9999`. A first attempt is to append a rule to `FORWARD` that allows `tcp/9999` arriving on `eth0` and leaving on `eth1`:

```shell
ubuntu@firewall:~$ iptables \
    -A FORWARD \
    -i eth0 \
    -o eth1 \
    -p tcp \
    --dport 9999 \
    -j ACCEPT
```

This rule alone is not enough. It only covers Transmission Control Protocol (TCP) packets destined to port `9999` from `eth0` to `eth1`, but not the return traffic. `client` can reach `web`, but `web`'s replies are dropped by `firewall`.

The fix is a stateful rule that allows packets belonging to a connection the firewall has already seen:

```shell
ubuntu@firewall:~$ iptables \
    -A FORWARD \
    -m conntrack \
    --ctstate ESTABLISHED,RELATED \
    -j ACCEPT
```

To test, listen on `web`

```shell
ubuntu@web:~$ nc -l -p 9999
```

and connect from `client`

```shell
ubuntu@client:~$ nc 10.20.30.100 9999
```

and bytes typed in `client`'s shell appear on `web`'s listener.

> [!note]
> In a real deployment, `client` would not know `web`'s private IP. [§2.5](#25-nat) closes that gap with `DNAT`.

### 2.5. NAT

> [!warning]
> This section adds `DNAT` to the `FORWARD` rules from [§2.4](#24-packet-filtering). The ports remain hypothetical — they are NOT what is required by [§1](#1-text).

`DNAT` rewrites the destination of an inbound packet. It runs in `PREROUTING`, before the routing decision and before `FORWARD`, so the packet enters the filter table with its rewritten destination. For example, to forward `tcp/9000` arriving on `eth0` to `10.20.30.100:9999`

```shell
ubuntu@firewall:~$ iptables \
    -t nat \
    -A PREROUTING \
    -i eth0 \
    -p tcp \
    --dport 9000 \
    -j DNAT \
    --to-destination 10.20.30.100:9999
```

> [!warning]
> Each `DNAT` rule must be paired with a `FORWARD` allow on the post-DNAT port — without it, the rewritten packet hits the default `DROP`.

`SNAT` rewrites the source address of outgoing packets. It runs in `POSTROUTING`, after the routing decision and after `FORWARD`, so that replies are routed back to `firewall` rather than to a private address that the remote host cannot reach. For example, to rewrite the source of every packet leaving `eth0` to the `firewall`'s public IP

```shell
ubuntu@firewall:~$ iptables \
    -t nat \
    -A POSTROUTING \
    -o eth0 \
    -j SNAT \
    --to-source 203.0.113.1
```

`MASQUERADE` is a variant of `SNAT` that also runs in `POSTROUTING` and automatically uses the address currently assigned to the outgoing interface. It is the right choice when that address is not statically known. For example, to masquerade all traffic leaving `eth0`

```shell
ubuntu@firewall:~$ iptables \
    -t nat \
    -A POSTROUTING \
    -o eth0 \
    -j MASQUERADE
```

### 2.6. Deliverable file

The deliverable is a plain text file containing all `iptables` commands, starting with the template from [§1](#1-text).

> [!tip]
> To inspect the rules currently loaded in the kernel and compare them against your file:
> ```shell
> $ iptables -S
> $ iptables -t nat -S
> ```

## 3. Solution

This exercise was proposed on [February 9, 2026](https://github.com/fglmtt/admin/tree/main/exams/2026-02-09/iptables).

## Licenses

| Content | License                                                                                                                       |
| ------- | ----------------------------------------------------------------------------------------------------------------------------- |
| Code    | [MIT License](https://mit-license.org/)                                                                                       |
| Text    | [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International](https://creativecommons.org/licenses/by-nc-sa/4.0/) |
