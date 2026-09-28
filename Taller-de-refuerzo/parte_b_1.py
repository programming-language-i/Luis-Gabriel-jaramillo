# Tarda 3 segundos en ejecutarse,porque join() dentro del bucle espera a cada hilo antes de lanzar el siguiente, así que queda secuencial (3 × 1 s). Para llegar a ~1 s hay que hacer primero todos los start() y después todos los join().
import threading
import time


def tarea(n):
    time.sleep(1)


inicio = time.perf_counter()
for i in range(3):
    hilo = threading.Thread(target=tarea, args=(i,))
    hilo.start()
    hilo.join()
print(f"{time.perf_counter() - inicio:.1f} s")