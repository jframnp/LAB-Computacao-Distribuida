from mpi4py import MPI
import random
import time

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

N = 10_000_000
N_local = N // size

comm.Barrier()
inicio = time.time()

dentro_local = 0
for _ in range(N_local):
    x = random.random()
    y = random.random()
    if x * x + y * y <= 1.0:
        dentro_local += 1

dentro_total = comm.reduce(dentro_local, op=MPI.SUM, root=0)

if rank == 0:
    total_pontos = N_local * size
    pi_estimado = 4.0 * dentro_total / total_pontos
    fim = time.time()
    print(f"PI aproximado: {pi_estimado:.6f}")
    print(f"Tempo distribuído MPI: {(fim - inicio) * 1000:.2f} ms")
