#El error queda guardado en futuro y nadie lo pide con futuro.result(), así que no se ve.

from concurrent.futures import ThreadPoolExecutor


def dividir(a, b):
    return a / b


with ThreadPoolExecutor() as pool:
    futuro = pool.submit(dividir, 1, 0)
print("listo")