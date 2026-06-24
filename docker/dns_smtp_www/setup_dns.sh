#!/bin/bash

set -eu

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
apt install -y bind9 bind9-utils dnsutils

mkdir -p /etc/bind

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
127.0.0.1;
172.17.0.0/16;
192.168.10.0/24;
};

allow-query-cache {
127.0.0.1;
172.17.0.0/16;
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

echo "===== Criando zona direta ====="

cat > /etc/bind/db.$DOMINIO <<EOF
\$TTL 86400

@ IN SOA ns1.$DOMINIO. admin.$DOMINIO. (
2026062101
21600
1800
604800
86400
)

@ IN NS ns1.$DOMINIO.

@ IN MX 10 mail.$DOMINIO.

ns1     IN A $IP_DNS
router  IN A $IP_ROTEADOR
www     IN A $IP_WWW
dhcp    IN A $IP_DHCP
mail    IN A $IP_SMTP

smtp    IN CNAME mail
imap    IN CNAME mail
pop3    IN CNAME mail

site    IN CNAME www
portal  IN CNAME www
EOF

echo "===== Criando zona reversa ====="

cat > /etc/bind/db.10.168.192 <<EOF
\$TTL 86400

@ IN SOA ns1.$DOMINIO. admin.$DOMINIO. (
2026062101
21600
1800
604800
86400
)

@ IN NS ns1.$DOMINIO.

254 IN PTR router.$DOMINIO.
2   IN PTR ns1.$DOMINIO.
3   IN PTR www.$DOMINIO.
4   IN PTR dhcp.$DOMINIO.
5   IN PTR mail.$DOMINIO.
EOF

echo "===== Ajustando permissões ====="

chown bind:bind /etc/bind/db.$DOMINIO
chown bind:bind /etc/bind/db.10.168.192

echo "===== Validando configuração ====="

named-checkconf

echo ""
echo "Validando zona direta..."
named-checkzone "$DOMINIO" "/etc/bind/db.$DOMINIO"

echo ""
echo "Validando zona reversa..."
named-checkzone "10.168.192.in-addr.arpa" "/etc/bind/db.10.168.192"

echo ""
echo "DNS configurado com sucesso"
echo ""

echo "===== Iniciando BIND ====="

exec named -g -u bind

