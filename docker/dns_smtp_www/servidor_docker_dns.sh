#!/bin/bash

set -e

EMPRESA="PipeVendas"
DOMINIO="pipevendas.com.br"

IP_ROTEADOR="192.168.10.254"
IP_DNS="192.168.10.2"
IP_WWW="192.168.10.3"
IP_DHCP="192.168.10.4"
IP_SMTP="192.168.10.5"

DNS_FORWARD1="8.8.8.8"
DNS_FORWARD2="1.1.1.1"
DNS_FORWARD3="9.9.9.9"

echo "===== Instalando BIND ====="

export DEBIAN_FRONTEND=noninteractive

apt update

apt install -y 
bind9 
bind9-utils 
dnsutils

echo "===== Configurando opções ====="

cat > /etc/bind/named.conf.options <<EOF
options {

directory "/var/cache/bind";

forwarders {
$DNS_FORWARD1;
$DNS_FORWARD2;
$DNS_FORWARD3;
};

forward only;

allow-recursion {
192.168.10.0/24;
};

allow-query {
any;
};

dnssec-validation auto;

listen-on {
any;
};

listen-on-v6 {
any;
};

allow-transfer {
none;
};

version "not available";

};

include "/etc/bind/named.conf.local";
EOF

echo "===== Configurando zonas ====="

cat > /etc/bind/named.conf.local <<EOF
zone "$DOMINIO" {
type master;
file "/etc/bind/db.$DOMINIO";
};

zone "10.168.192.in-addr.arpa" {
type master;
file "/etc/bind/db.10.168.192";
};
EOF

echo "===== Zona direta ====="

cat > /etc/bind/db.$DOMINIO <<EOF
$TTL 86400

@ IN SOA ns1.$DOMINIO. admin.$DOMINIO. (
2026062001
21600
1800
604800
86400
)

@ IN NS ns1.$DOMINIO.

@ IN MX 10 mail.$DOMINIO.

ns1 IN A $IP_DNS
router IN A $IP_ROTEADOR
www IN A $IP_WWW
dhcp IN A $IP_DHCP
mail IN A $IP_SMTP

smtp IN CNAME mail
imap IN CNAME mail
pop3 IN CNAME mail

site IN CNAME www
portal IN CNAME www
EOF

echo "===== Zona reversa ====="

cat > /etc/bind/db.10.168.192 <<EOF
$TTL 86400

@ IN SOA ns1.$DOMINIO. admin.$DOMINIO. (
2026062001
21600
1800
604800
86400
)

@ IN NS ns1.$DOMINIO.

254 IN PTR router.$DOMINIO.
2 IN PTR ns1.$DOMINIO.
3 IN PTR [www.$DOMINIO](http://www.$DOMINIO).
4 IN PTR dhcp.$DOMINIO.
5 IN PTR mail.$DOMINIO.
EOF

echo "===== Ajustando permissões ====="

chown bind:bind /etc/bind/db.$DOMINIO
chown bind:bind /etc/bind/db.10.168.192

echo "===== Validando ====="

named-checkconf

named-checkzone 
$DOMINIO 
/etc/bind/db.$DOMINIO

named-checkzone 
10.168.192.in-addr.arpa 
/etc/bind/db.10.168.192

echo ""
echo "DNS configurado"
echo ""

echo "===== Iniciando BIND ====="

exec named 
-g 
-u bind
