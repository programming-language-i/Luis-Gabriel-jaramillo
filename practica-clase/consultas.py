import random
import time
from concurrent.futures import ThreadPoolExecutor

# Lista de peticiones/APIs a consultar
PAGINAS = [f"https://api.ejemplo.com/producto/{i}" for i in range(1, 16)]


def consultar_api(url):
    tiempo_espera = random.uniform(0.5, 1.5)  # Simula latencia de red (I/O)
    time.sleep(tiempo_espera)
    return f"Respuesta de {url} (Tiempo respuesta: {tiempo_espera:.2f}s)"


if __name__ == "__main__":
    print(
        f"Iniciando {len(PAGINAS)} consultas concurrentes con ThreadPoolExecutor..."
    )

    inicio_tiempo = time.perf_counter()

    with ThreadPoolExecutor(max_workers=5) as executor:
        resultados = list(executor.map(consultar_api, PAGINAS))

    tiempo_total = time.perf_counter() - inicio_tiempo

    for res in resultados[:3]:  # Muestra algunas respuestas de muestra
        print(f"  - {res}")
    print(f"  ... y {len(resultados) - 3} consultas más.")

    print(f"Tiempo total de consultas: {tiempo_total:.2f} segundos")