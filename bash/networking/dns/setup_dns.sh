#!/bin/bash

set -e

# Configurações da empresa
EMPRESA="PipeVendas"
DOMINIO="pipevendas.com.br"
DNS_IP="172.16.0.2"

# Infraestrutura s-r1-r2-xy com redes diferentes
IP_SERVER="172.16.0.2"      # s - DNS Server (Rede A)
IP_ROUTER1="172.16.0.1"     # r1 - Roteador Principal (Rede A)
IP_ROUTER2="10.0.0.2"       # r2 - Roteador Secundário (Rede B)
IP_SERVER_X="192.168.0.1"   # x - Cliente X (Rede C)
IP_SERVER_Y="192.168.0.2"   # y - Cliente Y (Rede C)

# ============================================
# DHCP NO MESMO SERVIDOR QUE DNS
# ============================================
IP_DHCP="$IP_SERVER"  # 172.16.0.2 - Mesmo IP do DNS

# DNS públicos para forwarding
DNS_FORWARD1="8.8.8.8"
DNS_FORWARD2="1.1.1.1"
DNS_FORWARD3="9.9.9.9"

echo "========= Instalando BIND para $EMPRESA (DNS+DHCP no mesmo servidor) ========="

sudo apt update
sudo apt install -y bind9 bind9utils dnsutils

echo ""
echo "Configurando opções do BIND..."

sudo tee /etc/bind/named.conf.options > /dev/null <<EOF
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
        172.16.0.0/24;    // Rede A (s, r1, DHCP)
        10.0.0.0/24;      // Rede B (r2)
        192.168.0.0/24;   // Rede C (x, y)
        172.17.0.0/16;    // Docker
    };

    allow-query-cache {
        127.0.0.1;
        172.16.0.0/24;
        10.0.0.0/24;
        192.168.0.0/24;
        172.17.0.0/16;
    };

    allow-query { any; };
    
    dnssec-validation auto;
    listen-on { any; };
    listen-on-v6 { any; };
    allow-transfer { none; };
    version "not available";
};

include "/etc/bind/named.conf.local";
EOF

echo ""
echo "Configurando resolver..."

sudo tee /etc/resolv.conf > /dev/null <<EOF
domain $DOMINIO
search $DOMINIO
nameserver $DNS_IP
options ndots:0
EOF

if systemctl is-active systemd-resolved >/dev/null 2>&1; then
    sudo tee /etc/systemd/resolved.conf > /dev/null <<EOF
[Resolve]
DNS=$DNS_IP
Domains=$DOMINIO
EOF
    sudo systemctl restart systemd-resolved
fi

echo ""
echo "Configurando zonas locais (DNS+DHCP mesmo IP)..."

sudo tee /etc/bind/named.conf.local > /dev/null <<EOF
// Zona direta do domínio $DOMINIO
zone "$DOMINIO" {
    type master;
    file "/etc/bind/db.$DOMINIO";
    allow-update { 
        172.16.0.0/24;     // Rede A
        10.0.0.0/24;       // Rede B
        192.168.0.0/24;    // Rede C
        127.0.0.1;         // Localhost (DHCP no mesmo servidor)
    };
};

// Zona reversa para rede 172.16.0.0/24
zone "0.16.172.in-addr.arpa" {
    type master;
    file "/etc/bind/db.0.16.172";
    allow-update { 
        172.16.0.0/24;
        127.0.0.1;
    };
};

// Zona reversa para rede 10.0.0.0/24
zone "0.0.10.in-addr.arpa" {
    type master;
    file "/etc/bind/db.0.0.10";
};

// Zona reversa para rede 192.168.0.0/24
zone "0.168.192.in-addr.arpa" {
    type master;
    file "/etc/bind/db.0.168.192";
};

EOF

echo ""
echo "Criando zona direta para $DOMINIO (DNS+DHCP mesmo IP)..."

sudo tee /etc/bind/db.$DOMINIO > /dev/null <<EOF
\$TTL 86400

@ IN SOA s.$DOMINIO. admin.$DOMINIO. (
    2026062001
    21600
    1800
    604800
    86400
)

; Servidores DNS
@ IN NS s.$DOMINIO.
@ IN NS r1.$DOMINIO.

; Email
@ IN MX 10 mail.$DOMINIO.

; ============================================
; INFRAESTRUTURA s-r1-r2-xy
; ============================================

; Rede A (172.16.0.0/24) - DNS + DHCP
s       IN A $IP_SERVER
ns1     IN CNAME s.$DOMINIO.
dhcp    IN A $IP_DHCP      # DHCP no mesmo IP do DNS

r1      IN A $IP_ROUTER1
router  IN CNAME r1.$DOMINIO.
gateway IN CNAME r1.$DOMINIO.
ns2     IN CNAME r1.$DOMINIO.

; Rede B (10.0.0.0/24)
r2      IN A $IP_ROUTER2
router2 IN CNAME r2.$DOMINIO.

; Rede C (192.168.0.0/24)
x       IN A $IP_SERVER_X
app     IN CNAME x.$DOMINIO.
www     IN CNAME x.$DOMINIO.
site    IN CNAME x.$DOMINIO.
portal  IN CNAME x.$DOMINIO.

y       IN A $IP_SERVER_Y
db      IN CNAME y.$DOMINIO.
database IN CNAME y.$DOMINIO.

; Serviços
mail    IN A $IP_SERVER_X
smtp    IN CNAME mail.$DOMINIO.
pop3    IN CNAME mail.$DOMINIO.
imap    IN CNAME mail.$DOMINIO.

localhost IN A 127.0.0.1

EOF

echo ""
echo "Criando zonas reversas..."

# Zona Reversa - Rede A (172.16.0.0/24)
sudo tee /etc/bind/db.0.16.172 > /dev/null <<EOF
\$TTL 86400

@ IN SOA s.$DOMINIO. admin.$DOMINIO. (
    2026062001
    21600
    1800
    604800
    86400
)

@ IN NS s.$DOMINIO.
@ IN NS r1.$DOMINIO.

; Registros PTR para Rede A
1   IN PTR r1.$DOMINIO.
2   IN PTR s.$DOMINIO.
2   IN PTR dhcp.$DOMINIO.   # DHCP no mesmo IP
EOF

# Zona Reversa - Rede B (10.0.0.0/24)
sudo tee /etc/bind/db.0.0.10 > /dev/null <<EOF
\$TTL 86400

@ IN SOA s.$DOMINIO. admin.$DOMINIO. (
    2026062001
    21600
    1800
    604800
    86400
)

@ IN NS s.$DOMINIO.
@ IN NS r1.$DOMINIO.

; Registros PTR para Rede B
2   IN PTR r2.$DOMINIO.
EOF

# Zona Reversa - Rede C (192.168.0.0/24)
sudo tee /etc/bind/db.0.168.192 > /dev/null <<EOF
\$TTL 86400

@ IN SOA s.$DOMINIO. admin.$DOMINIO. (
    2026062001
    21600
    1800
    604800
    86400
)

@ IN NS s.$DOMINIO.
@ IN NS r1.$DOMINIO.

; Registros PTR para Rede C
1   IN PTR x.$DOMINIO.
1   IN PTR www.$DOMINIO.
1   IN PTR app.$DOMINIO.
2   IN PTR y.$DOMINIO.
2   IN PTR db.$DOMINIO.
EOF

echo ""
echo "Configurando permissões..."

sudo chown bind:bind /etc/bind/db.$DOMINIO
sudo chown bind:bind /etc/bind/db.0.16.172
sudo chown bind:bind /etc/bind/db.0.0.10
sudo chown bind:bind /etc/bind/db.0.168.192

echo ""
echo "Validando configuração..."

sudo named-checkconf
sudo named-checkzone $DOMINIO /etc/bind/db.$DOMINIO
sudo named-checkzone 0.16.172.in-addr.arpa /etc/bind/db.0.16.172
sudo named-checkzone 0.0.10.in-addr.arpa /etc/bind/db.0.0.10
sudo named-checkzone 0.168.192.in-addr.arpa /etc/bind/db.0.168.192

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Configuração validada com sucesso!"
else
    echo ""
    echo "❌ Erro na configuração. Corrija antes de reiniciar."
    exit 1
fi

echo ""
echo "Reiniciando BIND..."

sudo systemctl restart bind9
sudo systemctl enable bind9

echo ""
echo "=== CONFIGURAÇÃO DNS+DHCP CONCLUÍDA ==="
echo ""
echo "=== INFRAESTRUTURA ==="
echo "DNS + DHCP no mesmo servidor: $IP_SERVER"
echo ""
echo "🔴 IMPORTANTE: O script DHCP (isc-dhcp-server) deve ser configurado"
echo "   para escutar na interface 172.16.0.2 e fornecer IPs das redes:"
echo ""
echo "   subnet 172.16.0.0 netmask 255.255.255.0 {"
echo "       range 172.16.0.100 172.16.0.200;"
echo "       option routers 172.16.0.1;"
echo "       option domain-name-servers 172.16.0.2;"
echo "   }"
echo ""
echo "   subnet 10.0.0.0 netmask 255.255.255.0 {"
echo "       range 10.0.0.100 10.0.0.200;"
echo "       option routers 10.0.0.1;"
echo "       option domain-name-servers 172.16.0.2;"
echo "   }"
echo ""
echo "   subnet 192.168.0.0 netmask 255.255.255.0 {"
echo "       range 192.168.0.100 192.168.0.200;"
echo "       option routers 192.168.0.1;"
echo "       option domain-name-servers 172.16.0.2;"
echo "   }"
echo ""
echo "=== TESTES ==="
echo ""
echo "Teste de resolução:"
echo "  host s.$DOMINIO        # 172.16.0.2"
echo "  host dhcp.$DOMINIO     # 172.16.0.2 (mesmo IP)"
echo "  host r2.$DOMINIO       # 10.0.0.2"
echo "  host www.$DOMINIO      # 192.168.0.1"
echo ""
echo "Teste reverso:"
echo "  host 172.16.0.2        # s.$DOMINIO e dhcp.$DOMINIO"
echo ""
echo "Concluído."