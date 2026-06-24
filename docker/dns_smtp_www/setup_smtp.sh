#!/bin/bash

set -e

DOMINIO="pipevendas.com.br"
USUARIO="joao.silva"
SENHA="123456"

echo "===== Atualizando pacotes ====="

export DEBIAN_FRONTEND=noninteractive

apt update

echo "===== Instalando Postfix ====="

debconf-set-selections <<EOF
postfix postfix/mailname string $DOMINIO
postfix postfix/main_mailer_type string Internet Site
EOF

apt install -y 
postfix 
mailutils

echo "===== Configurando SMTP ====="

postconf -e "myhostname=mail.$DOMINIO"

postconf -e "mydomain=$DOMINIO"

postconf -e "myorigin=$mydomain"

postconf -e "inet_interfaces=all"

postconf -e "inet_protocols=ipv4"

postconf -e "mydestination=$myhostname, localhost.$mydomain, localhost, $mydomain"

postconf -e "home_mailbox=Maildir/"

postconf -e "local_recipient_maps="

echo "===== Criando usuário ====="

if ! id "$USUARIO" >/dev/null 2>&1
then

useradd -m "$USUARIO"

echo "$USUARIO:$SENHA" | chpasswd

fi

echo "===== Criando Maildir ====="

mkdir -p "/home/$USUARIO/Maildir"

chown -R "$USUARIO:$USUARIO" "/home/$USUARIO/Maildir"

echo "===== Validando configuração ====="

postfix check

echo ""
echo "SMTP pronto"
echo ""

echo "Usuário:"
echo "$USUARIO@$DOMINIO"

echo ""

echo "Iniciando Postfix..."

postfix start

tail -f /var/log/mail.log
