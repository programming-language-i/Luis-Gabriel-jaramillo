#Un hilo que ya terminó no se puede volver a iniciar. 

import threading

hilo = threading.Thread(target=print, args=("hola",))
hilo.start()
hilo.join()
print(hilo.is_alive())
hilo.start()