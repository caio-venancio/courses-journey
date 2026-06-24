#!/bin/bash
# backup-dns-config.sh
# Execute ANTES de instalar o BIND personalizado

echo "========================================="
echo "  FAZENDO BACKUP DAS CONFIGURAÇÕES DNS"
echo "========================================="

DATA=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/root/backup-dns-$DATA"

# Criar diretório de backup
mkdir -p "$BACKUP_DIR"

# 1. Backup dos arquivos de configuração do BIND
if [ -d /etc/bind ]; then
    echo "Fazendo backup de /etc/bind..."
    cp -r /etc/bind "$BACKUP_DIR/"
    
    # Backup específico dos arquivos principais
    cp /etc/bind/named.conf.options "$BACKUP_DIR/named.conf.options.original" 2>/dev/null || echo "  (named.conf.options não encontrado)"
    cp /etc/bind/named.conf.local "$BACKUP_DIR/named.conf.local.original" 2>/dev/null || echo "  (named.conf.local não encontrado)"
    cp /etc/bind/named.conf "$BACKUP_DIR/named.conf.original" 2>/dev/null || echo "  (named.conf não encontrado)"
fi

# 2. Backup do resolv.conf
echo "Fazendo backup de /etc/resolv.conf..."
cp /etc/resolv.conf "$BACKUP_DIR/resolv.conf.original" 2>/dev/null || echo "  (resolv.conf não encontrado)"

# 3. Backup do systemd-resolved (se existir)
if [ -f /etc/systemd/resolved.conf ]; then
    echo "Fazendo backup de /etc/systemd/resolved.conf..."
    cp /etc/systemd/resolved.conf "$BACKUP_DIR/resolved.conf.original"
fi

# 4. Lista de pacotes instalados
echo "Salvando lista de pacotes..."
dpkg -l | grep bind > "$BACKUP_DIR/pacotes-bind.txt"

echo ""
echo "========================================="
echo "  ✅ BACKUP CONCLUÍDO!"
echo "========================================="
echo ""
echo "Backup salvo em: $BACKUP_DIR"
echo ""
echo "Arquivos salvos:"
ls -la "$BACKUP_DIR"
echo ""
echo "Para restaurar manualmente, use:"
echo "  sudo cp $BACKUP_DIR/named.conf.options.original /etc/bind/named.conf.options"
echo "  sudo cp $BACKUP_DIR/named.conf.local.original /etc/bind/named.conf.local"
echo "  sudo cp $BACKUP_DIR/resolv.conf.original /etc/resolv.conf"
echo ""
echo "Ou execute o script de restauração:"
echo "  sudo ./restaurar-backup-dns.sh $BACKUP_DIR"