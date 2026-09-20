from mpi4py import MPI
import random
import time

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

N = 1000

A = None
B = None

if rank == 0:
    A = [[random.random() for _ in range(N)] for _ in range(N)]
    B = [[random.random() for _ in range(N)] for _ in range(N)]

comm.Barrier()
inicio = time.time()

A = comm.bcast(A, root=0)
B = comm.bcast(B, root=0)

linhas_por_processo = N // size
inicio_linha = rank * linhas_por_processo
fim_linha = N if rank == size - 1 else (rank + 1) * linhas_por_processo

C_local = []
for i in range(inicio_linha, fim_linha):
    linha_resultado = [0.0] * N
    for j in range(N):
        soma = 0.0
        for k in range(N):
            soma += A[i][k] * B[k][j]
        linha_resultado[j] = soma
    C_local.append(linha_resultado)

resultados = comm.gather(C_local, root=0)

if rank == 0:
    C = []
    for parte in resultados:
        C.extend(parte)
    fim = time.time()
    print(f"Matriz {N}x{N} multiplicada com {size} processos MPI.")
    print(f"Tempo distribuído MPI: {(fim - inicio) * 1000:.2f} ms")
