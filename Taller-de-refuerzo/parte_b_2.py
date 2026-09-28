#Al terminar el hilo principal tras 0.5 s, la aplicación muere inmediatamente por ser el único hilo superviviente daemon, interrumpiéndolo antes de llegar a los 2 s y sin ejecutar el finally.

import threading
import time


def guardar():
    try:
        time.sleep(2)
        print("guardado")
    finally:
        print("archivo cerrado")


threading.Thread(target=guardar, daemon=True).start()
time.sleep(0.5)
print("fin")