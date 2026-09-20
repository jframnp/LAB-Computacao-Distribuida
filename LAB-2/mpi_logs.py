from mpi4py import MPI
import random

# Inicialização do MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()


# Função para gerar logs

def gerar_logs(qtd):
    ips = [f"192.168.1.{i}" for i in range(2,254)]
    endpoints = [
        "/",
        "/login",
        "/products",
        "/cart",
        "/checkout",
        "/api/users",
        "/api/orders"
    ]

    metodos = ["GET", "POST"]
    status = ["200", "200", "200", "404", "500"]

    logs = []
    # INSIRA AQUI O SEU CÓDIGO PARA GERAR OS DADOS DO LOG
    # RANDOMIZE OS IPS, ENDPOINTS, METODOS E STATUS
    for _ in range(qtd):
        ip = random.choice(ips)
        metodo = random.choice(metodos)
        endpoint = random.choice(endpoints)
        stat = random.choice(status)
        linha = f"{ip} {metodo} {endpoint} {stat}"
        logs.append(linha)
    return logs


# Processo 0 gera o dataset

logs_divididos = None
TOTAL_LOGS = 100000

if rank == 0:
    print("\nGerando dataset de logs...\n")
    logs = gerar_logs(TOTAL_LOGS)
    # DIVIDIR AQUI O DATASET ENTRE OS PROCESSOS
    # O NÓ MASTER TAMBÉM PROCESSA SUA PARTE DO DATASET
    tamanho_fatia = len(logs) // size
    logs_divididos = [
        logs[i * tamanho_fatia: (i + 1) * tamanho_fatia]
        for i in range(size)
    ]


# Distribuição usando Scatter

# DISTRIBUIR OS DADOS USANDO SCATTER
logs_locais = comm.scatter(logs_divididos, root=0)

# Processamento local em cada nó

# INSIRA AQUI O CÓDIGO DE PROCESSAMENTO LOCAL DO LOG
erros = 0
for linha in logs_locais:
    campos = linha.split()
    status_code = campos[3]
    if status_code == "404" or status_code == "500":
        erros += 1

# Nós Master
# Imprime os resultados de cada nó worker e seu também

# A variável 'logs_locais' representa a fatia recebida e 'erros' o contador
print(f"Processo {rank} analisou {len(logs_locais)} linhas "
      f"e encontrou {erros} erros.")