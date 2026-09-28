import math
import time
from concurrent.futures import ProcessPoolExecutor


def es_primo(n):
    if n < 2:
        return False
    for i in range(2, int(math.isqrt(n)) + 1):
        if n % i == 0:
            return False
    return True


def contar_primos_en_rango(rango):
    inicio, fin = rango
    return sum(1 for i in range(inicio, fin) if es_primo(i))


if __name__ == "__main__":
    RANGO_MAX = 2_000_000
    LANK_TAMAÑO = 500_000

    # Crear rangos de trabajo
    rangos = [
        (i, min(i + LANK_TAMAÑO, RANGO_MAX))
        for i in range(0, RANGO_MAX, LANK_TAMAÑO)
    ]

    print(f"Buscando números primos hasta {RANGO_MAX:,} usando Procesos...")

    inicio_tiempo = time.perf_counter()

    with ProcessPoolExecutor(max_workers=4) as executor:
        resultados = list(executor.map(contar_primos_en_rango, rangos))

    total_primos = sum(resultados)
    tiempo_total = time.perf_counter() - inicio_tiempo

    print(f"Total de primos encontrados: {total_primos:,}")
    print(f"Tiempo de ejecución: {tiempo_total:.2f} segundos")