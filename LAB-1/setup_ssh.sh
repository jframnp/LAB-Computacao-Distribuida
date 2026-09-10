#!/bin/bash

echo "Gerando chave no master..."

# Gera a chave SSH no container master sem senha
docker compose exec master sudo -u mpiuser ssh-keygen -t rsa -N "" -f /home/mpiuser/.ssh/id_rsa

# Captura a chave pública gerada
PUBKEY=$(docker compose exec master cat /home/mpiuser/.ssh/id_rsa.pub)

# Distribui a chave pública para os nós trabalhadores
for node in worker1 worker2 worker3; do
    echo "Configurando $node..."
    
    echo "$PUBKEY" | docker compose exec -T $node bash -c "
        mkdir -p /home/mpiuser/.ssh &&
        cat >> /home/mpiuser/.ssh/authorized_keys &&
        chown -R mpiuser:mpiuser /home/mpiuser/.ssh &&
        chmod 700 /home/mpiuser/.ssh &&
        chmod 600 /home/mpiuser/.ssh/authorized_keys
    "
done

echo "SSH configurado com sucesso!"

