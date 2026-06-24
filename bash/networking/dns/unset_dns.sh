#!/bin/bash

# Script de DESINSTALAÇÃO do BIND9
# Remove todas as configurações e volta ao estado original

set -e

echo "===================================================="
echo "   DESINSTALANDO BIND9 E LIMPANDO CONFIGURAÇÕES"
echo "===================================================="

# 1. Parar e desabilitar o serviço
echo ""
echo "[1/6] Parando e desabilitando BIND9..."
sudo systemctl stop bind9 2>/dev/null || true
sudo systemctl disable bind9 2>/dev/null || true

# 2. Remover os pacotes
echo ""
echo "[2/6] Removendo BIND9 e utilitários..."
sudo apt remove --purge -y bind9 bind9utils dnsutils
sudo apt autoremove -y

# 3. Remover arquivos de configuração criados
echo ""
echo "[3/6] Removendo arquivos de configuração..."
sudo rm -f /etc/bind/db.pipevendas.com.br
sudo rm -f /etc/bind/db.10.168.192
sudo rm -f /etc/bind/db.0.16.172
sudo rm -f /etc/bind/db.0.0.10
sudo rm -f /etc/bind/db.0.168.192

# 4. Restaurar arquivos de configuração do BIND
echo ""
echo "[4/6] Restaurando configurações originais do BIND..."

# Restaurar named.conf.options original (se existir backup)
if [ -f /etc/bind/named.conf.options.default ]; then
    sudo cp /etc/bind/named.conf.options.default /etc/bind/named.conf.options
else
    # Criar um named.conf.options básico
    sudo tee /etc/bind/named.conf.options > /dev/null <<EOF
options {
    directory "/var/cache/bind";

    // If there is a firewall between you and nameservers you want
    // to talk to, you may need to fix the firewall to allow multiple
    // ports to talk.  See http://www.kb.cert.org/vuls/id/800113

    // If your ISP provided one or more IP addresses for stable 
    // nameservers, you probably want to use them as forwarders.
    // Uncomment the following block, and insert the addresses replacing 
    // the all-0's placeholder.

    // forwarders {
    // 	0.0.0.0;
    // };

    //========================================================================
    // If BIND logs error messages about the root key being expired,
    // you will need to update your keys.  See https://www.isc.org/bind-keys
    //========================================================================
    dnssec-validation auto;

    listen-on-v6 { any; };
};
EOF
fi

# Restaurar named.conf.local original (se existir backup)
if [ -f /etc/bind/named.conf.local.default ]; then
    sudo cp /etc/bind/named.conf.local.default /etc/bind/named.conf.local
else
    # Criar um named.conf.local vazio
    sudo tee /etc/bind/named.conf.local > /dev/null <<EOF
//
// Do any local configuration here
//

// Consider adding the 1918 zones here, if they are not used in your
// organization
//include "/etc/bind/zones.rfc1918";
EOF
fi

# 5. Restaurar o resolv.conf original
echo ""
echo "[5/6] Restaurando /etc/resolv.conf..."

# Fazer backup do resolv.conf atual
sudo cp /etc/resolv.conf /etc/resolv.conf.bkp.$(date +%Y%m%d_%H%M%S)

if systemctl is-active systemd-resolved >/dev/null 2>&1; then
    # Se estiver usando systemd-resolved, restaura configuração padrão
    sudo tee /etc/systemd/resolved.conf > /dev/null <<EOF
[Resolve]
DNS=
Domains=
#FallbackDNS=8.8.8.8 1.1.1.1
#LLMNR=no
#MulticastDNS=no
#DNSSEC=no
#DNSOverTLS=no
#Cache=yes
#DNSStubListener=yes
EOF
    sudo systemctl restart systemd-resolved
    echo "  systemd-resolved reiniciado com configuração padrão"
else
    # Se não tiver systemd-resolved, restaura para o padrão do Ubuntu
    sudo tee /etc/resolv.conf > /dev/null <<EOF
nameserver 8.8.8.8
nameserver 1.1.1.1
EOF
fi

# 6. Remover logs e arquivos temporários
echo ""
echo "[6/6] Limpando logs e arquivos temporários..."
sudo rm -f /var/log/bind/*.log 2>/dev/null || true
sudo rm -f /etc/bind/*.jnl 2>/dev/null || true
sudo rm -f /etc/bind/*.bak 2>/dev/null || true

echo ""
echo "===================================================="
echo "   ✅ DESINSTALAÇÃO CONCLUÍDA!"
echo "===================================================="
echo ""
echo "O que foi removido:"
echo "  ✅ Pacotes BIND9 e utilitários"
echo "  ✅ Arquivos de zona criados"
echo "  ✅ Configurações personalizadas"
echo "  ✅ Arquivos de log"
echo ""
echo "O que foi restaurado:"
echo "  ✅ Configurações padrão do BIND"
echo "  ✅ resolv.conf para DNS externo (8.8.8.8)"
echo "  ✅ systemd-resolved (se aplicável)"
echo ""
echo "⚠️  Recomendação:"
echo "  Reinicie o sistema para garantir que todas as"
echo "  mudanças sejam aplicadas corretamente."
echo ""
echo "  sudo reboot"
echo ""
echo "Para verificar se o BIND foi completamente removido:"
echo "  dpkg -l | grep bind"
echo "  systemctl status bind9"
echo ""

# Perguntar se quer reiniciar agora
read -p "Deseja reiniciar o sistema agora? (s/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Ss]$ ]]; then
    echo "Reiniciando sistema..."
    sudo reboot
else
    echo "Lembre-se de reiniciar o sistema depois para aplicar todas as mudanças."
fi