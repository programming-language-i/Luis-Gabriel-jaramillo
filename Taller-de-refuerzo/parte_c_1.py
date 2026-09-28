#Descarga por herencia.Qué pasa: Arroja RuntimeError o falla silenciosamente sin inicializar correctamente la clase base.
#Por qué: No se llamó al constructor de la clase madre super().__init__()
#Cambio mínimo: Agregar la línea super().__init__() dentro de __init__.

import threading


class Descarga(threading.Thread):
    def __init__(self, archivo):
        self.archivo = archivo

    def run(self):
        print("descargando", self.archivo)


Descarga("a.zip").start()