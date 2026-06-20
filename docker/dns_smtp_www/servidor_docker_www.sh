#!/bin/bash

set -e

DOMINIO="pipevendas.com.br"
ROOT="/var/www/$DOMINIO"

echo "===== Atualizando pacotes ====="

export DEBIAN_FRONTEND=noninteractive

apt update
apt install -y apache2

echo "===== Criando estrutura do site ====="

mkdir -p "$ROOT"

echo "===== Criando página inicial ====="

cat > "$ROOT/index.html" <<EOF

<!DOCTYPE html>

<html>
<head>
<meta charset="UTF-8">
<title>PipeVendas</title>
</head>

<body>

<h1>PipeVendas</h1>

<p>Servidor WWW funcionando em container Docker.</p>

<ul>
<li>Domínio: pipevendas.com.br</li>
<li>Servidor Apache</li>
<li>Projeto Fundamentos de Redes</li>
</ul>

</body>
</html>
EOF

echo "===== Configurando VirtualHost ====="

cat > "/etc/apache2/sites-available/$DOMINIO.conf" <<EOF
<VirtualHost *:80>

ServerName pipevendas.com.br
ServerAlias [www.pipevendas.com.br](http://www.pipevendas.com.br)

DocumentRoot $ROOT

<Directory $ROOT>
Options Indexes FollowSymLinks
AllowOverride All
Require all granted </Directory>

ErrorLog ${APACHE_LOG_DIR}/pipevendas_error.log
CustomLog ${APACHE_LOG_DIR}/pipevendas_access.log combined

</VirtualHost>
EOF

echo "===== Habilitando site ====="

a2dissite 000-default.conf || true
a2ensite "$DOMINIO.conf"

echo "===== Validando ====="

apache2ctl configtest

echo "===== Iniciando Apache ====="

exec apachectl -D FOREGROUND
