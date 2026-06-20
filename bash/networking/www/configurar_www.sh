#!/bin/bash

set -e

DOMINIO="pipevendas.com.br"
ROOT="/var/www/$DOMINIO"

echo "=====  Atualizando pacotes... ====="
sudo apt update

echo "===== Instalando Apache... ====="
sudo apt install apache2 -y

echo "===== Criando estrutura do site... ====="
sudo mkdir -p "$ROOT"

echo "===== Criando página inicial... ====="

sudo tee "$ROOT/index.html" > /dev/null <<EOF

<!DOCTYPE html>

<html>
<head>
<meta charset="UTF-8">
<title>PipeVendas</title>
</head>

<body>
<h1>PipeVendas</h1>

<p>Servidor WWW funcionando.</p>

<ul>
<li>Domínio: pipevendas.com.br</li>
<li>Servidor Apache</li>
<li>Projeto Fundamentos de Redes</li>
</ul>

</body>
</html>
EOF

echo "===== Configurando VirtualHost... ====="

sudo tee "/etc/apache2/sites-available/$DOMINIO.conf" > /dev/null <<EOF
<VirtualHost *:80>

```
ServerName pipevendas.com.br
ServerAlias www.pipevendas.com.br

DocumentRoot $ROOT

<Directory $ROOT>
    Options Indexes FollowSymLinks
    AllowOverride All
    Require all granted
</Directory>

ErrorLog \${APACHE_LOG_DIR}/pipevendas_error.log
CustomLog \${APACHE_LOG_DIR}/pipevendas_access.log combined
```

</VirtualHost>
EOF

echo "===== Habilitando site... ====="

sudo a2dissite 000-default.conf || true
sudo a2ensite "$DOMINIO.conf"

echo "===== Validando... ====="

sudo apache2ctl configtest

echo "===== Reiniciando Apache... ====="

sudo systemctl restart apache2
sudo systemctl enable apache2

echo ""
echo "Servidor configurado!"
echo ""
echo "Teste:"
echo "http://pipevendas.com.br"
echo ""
echo "Se DNS ainda não existir:"
echo "http://localhost"
