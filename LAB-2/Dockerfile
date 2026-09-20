FROM python:3.11-slim

# Instala o OpenMPI (necessário para o mpi4py funcionar)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libopenmpi-dev \
    openmpi-bin \
    && rm -rf /var/lib/apt/lists/*

# Instala o mpi4py
RUN pip install --no-cache-dir mpi4py

# Diretório de trabalho dentro do container
WORKDIR /app

# Copia o script para dentro do container
COPY mpi_logs.py .

# Comando padrão: executa o programa com 4 processos MPI
# (pode ser sobrescrito na hora do "docker run")
CMD ["mpirun", "--allow-run-as-root", "--oversubscribe", "-n", "4", "python3", "mpi_logs.py"]
