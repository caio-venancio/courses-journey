#!/bin/bash
# restaurar-backup-dns.sh
# Execute para restaurar as configurações a partir do backup

if [ -z "$1" ]; then
    echo "Uso: $0 <diretorio_backup>"
    echo "Exemplo: $0 /root/backup-dns-20260123_143022"
    exit 1
fi

BACKUP_DIR="$1"

echo "========================================="
echo "  RESTAURANDO CONFIGURAÇÕES DNS"
echo "========================================="

if [ ! -d "$BACKUP_DIR" ]; then
    echo "❌ Diretório de backup não encontrado: $BACKUP_DIR"
    exit 1
fi

echo "Restaurando de: $BACKUP_DIR"

# Restaurar configurações do BIND
if [ -f "$BACKUP_DIR/named.conf.options.original" ]; then
    echo "Restaurando named.conf.options..."
    sudo cp "$BACKUP_DIR/named.conf.options.original" /etc/bind/named.conf.options
    echo "  ✅ Restaurado"
fi

if [ -f "$BACKUP_DIR/named.conf.local.original" ]; then
    echo "Restaurando named.conf.local..."
    sudo cp "$BACKUP_DIR/named.conf.local.original" /etc/bind/named.conf.local
    echo "  ✅ Restaurado"
fi

# Restaurar resolv.conf
if [ -f "$BACKUP_DIR/resolv.conf.original" ]; then
    echo "Restaurando /etc/resolv.conf..."
    sudo cp "$BACKUP_DIR/resolv.conf.original" /etc/resolv.conf
    echo "  ✅ Restaurado"
fi

# Restaurar systemd-resolved
if [ -f "$BACKUP_DIR/resolved.conf.original" ]; then
    echo "Restaurando /etc/systemd/resolved.conf..."
    sudo cp "$BACKUP_DIR/resolved.conf.original" /etc/systemd/resolved.conf
    sudo systemctl restart systemd-resolved
    echo "  ✅ Restaurado"
fi

echo ""
echo "========================================="
echo "  ✅ RESTAURAÇÃO CONCLUÍDA!"
echo "========================================="
echo ""
echo "Recomendação: Reinicie o BIND se ainda estiver instalado"
echo "  sudo systemctl restart bind9"