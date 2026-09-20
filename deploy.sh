#!/bin/bash
set -e

echo ">> Subindo os containers do cluster (master + 3 workers)..."
docker compose up -d --build

echo ">> Iniciando o serviço SSH em cada nó..."
for node in master worker1 worker2 worker3; do
  docker compose exec -u root "$node" service ssh start
done

echo ">> Copiando os scripts para todos os nós..."
for node in master worker1 worker2 worker3; do
  docker cp exercicio1.py "$node":/home/mpiuser/
  docker cp exercicio2.py "$node":/home/mpiuser/
done

echo ""
echo ">> Cluster pronto! Para rodar o Exercício 1 (matrizes):"
echo '   docker compose exec master su - mpiuser -c "mpirun --hostfile hosts -np 4 python3 exercicio1.py"'
echo ""
echo ">> Para rodar o Exercício 2 (Monte Carlo):"
echo '   docker compose exec master su - mpiuser -c "mpirun --hostfile hosts -np 4 python3 exercicio2.py"'
