#!/bin/bash

apt update
apt install -y socat iproute2

ip maddr add 239.1.1.1 dev eth0

echo "Entrou no grupo"

socat \
UDP4-RECV:5000,ip-add-membership=239.1.1.1:0.0.0.0 \
STDOUT