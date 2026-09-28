#Un pool de procesos sin guarda.Qué pasa: En la mayoría de sistemas lanza BrokenProcessPool o entra en un bucle infinito de creación de procesos.
#Por qué: ProcessPoolExecutor requiere importar el módulo e iniciar los procesos hijos de manera segura dentro de la guarda principal.
#Cambio mínimo: Indentar el código del with dentro de un bloque if __name__ == "__main__":.

from concurrent.futures import ProcessPoolExecutor


def cuadrado(n):
    return n * n


with ProcessPoolExecutor(max_workers=2) as pool:
    print(list(pool.map(cuadrado, range(4))))