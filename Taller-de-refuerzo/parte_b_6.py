#total es estado de instancia (cada hilo el suyo). eventos es estado de clase, compartido: 3 + 3 = 6 elementos.

import threading


class Contador(threading.Thread):
    eventos = []

    def __init__(self, nombre):
        super().__init__(name=nombre)
        self.total = 0

    def run(self):
        for _ in range(3):
            self.total += 1
            self.eventos.append(self.name)


a, b = Contador("a"), Contador("b")
for h in (a, b):
    h.start()
for h in (a, b):
    h.join()
print(a.total, b.total, len(a.eventos))