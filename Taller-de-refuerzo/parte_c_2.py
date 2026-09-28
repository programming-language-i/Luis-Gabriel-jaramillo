#Tres tareas "concurrentes". Qué pasa: Muestra 3.0 s y ejecuta de forma secuencial.
#Por qué: Se sobrescribió el método start() reemplazando la creación del hilo de sistema por ejecución síncrona en el hilo principal.
#Cambio mínimo: Renombrar el método def start(self): por def run(self):.

import threading
import time


class Tarea(threading.Thread):
    def start(self):
        time.sleep(1)
        print(self.name, "lista")


inicio = time.perf_counter()
tareas = [Tarea(name=f"t{i}") for i in range(3)]
for t in tareas:
    t.start()
print(f"{time.perf_counter() - inicio:.1f} s")
for t in tareas:
    t.join()