#!/bin/bash

set -e

DOMINIO="pipevendas.com.br"
USUARIO="joao.silva"
SENHA="123456"

echo "===== Atualizando pacotes ====="

sudo apt update

echo "===== Instalando SMTP ====="

export DEBIAN_FRONTEND=noninteractive

sudo debconf-set-selections <<EOF
postfix postfix/mailname string $DOMINIO
postfix postfix/main_mailer_type string Internet Site
EOF

sudo apt install -y postfix mailutils

echo "===== Configurando Postfix ====="

sudo postconf -e "myhostname=mail.$DOMINIO"

sudo postconf -e "mydomain=$DOMINIO"

sudo postconf -e "myorigin=$mydomain"

sudo postconf -e "inet_interfaces=all"

sudo postconf -e "mydestination=$myhostname, localhost.$mydomain, localhost, $mydomain"

sudo postconf -e "home_mailbox=Maildir/"

sudo postconf -e "local_recipient_maps="

sudo systemctl restart postfix
sudo systemctl enable postfix

echo "===== Criando usuário de teste ====="

if ! id "$USUARIO" >/dev/null 2>&1
then

sudo useradd -m "$USUARIO"

echo "$USUARIO:$SENHA" | sudo chpasswd

fi

echo "===== Criando Maildir ====="

sudo -u "$USUARIO" mkdir -p "/home/$USUARIO/Maildir"

sudo -u "$USUARIO" maildirmake.dovecot "/home/$USUARIO/Maildir"

echo "===== Finalizado ====="

echo ""
echo "Servidor SMTP pronto"
echo ""

echo "Email criado:"
echo "$USUARIO@$DOMINIO"

echo ""
echo "Senha:"
echo "$SENHA"

echo ""
echo "Teste envio:"
echo ""

echo 'echo "teste" | mail -s "oi" [joao.silva@pipevendas.com.br](mailto:joao.silva@pipevendas.com.br)'
