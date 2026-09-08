# first name and last name: mattia fogli
# student id: 123456
#
# path: /etc/sudoers.d/site

Host_Alias  WEB = web01, web02, web03
Host_Alias  DB  = db01, db02

Cmnd_Alias  FWTOOLS = /usr/sbin/iptables, /usr/bin/tcpdump
Cmnd_Alias  ACCTMGM = /usr/sbin/useradd, /usr/sbin/usermod
Cmnd_Alias  PKGMGM  = /usr/bin/apt, /usr/bin/dpkg

alma        ALL  = (ALL) ALL
bruno       ALL  = (ALL) ALL, !FWTOOLS
%acct       WEB  = ACCTMGM
%pkg        DB   = NOPASSWD: PKGMGM
cleo        ALL  = NOPASSWD: /usr/bin/cat /etc/gshadow
dario       db01 = (elin) /usr/bin/id
%net, %pkg  ALL  = NOPASSWD: /usr/sbin/ip
