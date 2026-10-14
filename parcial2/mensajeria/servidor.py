"""
PARCIAL 2 - Nivel 2 · Servidor concurrente

    python3 -m mensajeria.servidor            escucha en el puerto 8000
    python3 -m mensajeria.servidor 8050       o en el que se le diga

Tal como está, el servidor acepta conexiones y no hace nada con ellas. Falta
el hilo por conexión y la atención del cliente.

Requisitos:
  1. Un hilo por conexión. El hilo principal solo acepta.
  2. La primera trama del cliente es su nombre. El servidor responde "OK" y lo
     registra, o responde "ERROR: nombre en uso" y cierra la conexión.
  3. Cada trama siguiente se retransmite a todos los demás como
     "emisor: contenido".
  4. El envío va FUERA del lock: se copia la lista de destinatarios bajo el
     lock y se envía después.
  5. Una desconexión no tumba nada: si un cliente se va, con aviso o a la
     fuerza, su entrada se borra del registro y los demás siguen. Un
     destinatario al que ya no se puede enviar también se retira.
  6. SO_REUSEADDR y `with` para los sockets.

Se comprueba con:   python3 prueba_n2.py   (desde la carpeta parcial2/)

Nivel 3: copie este archivo, ya resuelto, a mensajeria/servidor_json.py y
trabaje sobre la copia.
"""

import socket
import sys
import threading

from mensajeria.protocolo import enviar_mensaje, recibir_mensaje
from mensajeria.registro import RegistroClientes

HOST = "127.0.0.1"
PUERTO = 8000


def retransmitir(registro: RegistroClientes, emisor: str, texto: str) -> None:
    """Envía "emisor: texto" a todos los conectados menos al emisor."""
    mensaje = f"{emisor}: {texto}"
    destinatarios = registro.destinatarios(excepto=emisor)
    for nombre_dest, dest_sock in destinatarios:
        try:
            enviar_mensaje(dest_sock, mensaje)
        except OSError:
            registro.borrar(nombre_dest)


def atender(
    conexion: socket.socket, direccion: tuple[str, int], registro: RegistroClientes
) -> None:
    """Atiende a UN cliente, en su propio hilo, hasta que se desconecta."""
    nombre = None
    registrado = False  # <-- Bandera para saber si logró registrarse

    with conexion:
        try:
            # 1. Recibir la primera trama con el nombre
            nombre = recibir_mensaje(conexion)
            if not nombre:
                return

            # 2. Registrar el nombre; responder OK o ERROR
            if not registro.insertar(nombre, conexion):
                enviar_mensaje(conexion, "ERROR: nombre en uso")
                return  # Si falla, registrado se queda en False y no borrará a nadie en el finally

            registrado = True  # <-- Marcamos como registrado con éxito
            enviar_mensaje(conexion, "OK")

            # 3. Bucle para recibir y retransmitir tramas
            while True:
                texto = recibir_mensaje(conexion)
                if texto is None:
                    break
                retransmitir(registro, nombre, texto)

        except OSError:
            pass
        finally:
            # 4. SOLO se borra del registro si este hilo SÍ logró registrarlo
            if registrado and nombre:
                registro.borrar(nombre)


def main() -> None:
    # Las pruebas arrancan el servidor con un puerto libre: no cambie esta línea.
    puerto = int(sys.argv[1]) if len(sys.argv) > 1 else PUERTO
    registro = RegistroClientes()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
        servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        servidor.bind((HOST, puerto))
        servidor.listen()
        print(f"escuchando en {HOST}:{puerto}")
        while True:
            conexion, direccion = servidor.accept()
            # Se lanza un hilo independiente por cada conexión entrante
            hilo = threading.Thread(
                target=atender, args=(conexion, direccion, registro), daemon=True
            )
            hilo.start()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nservidor detenido")