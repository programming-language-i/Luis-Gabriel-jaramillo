# Módulo encargado de crear el socket del servidor en la red local
import socket

def crear_socket_servidor(host: str = '127.0.0.1', puerto: int = 8000) -> socket.socket:
    # Creamos un socket de tipo TCP (IPv4)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Permite reutilizar el puerto de forma inmediata si se reinicia el servidor
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # Vinculamos la dirección IP y el puerto
    sock.bind((host, puerto))
    # Ponemos el servidor a escuchar conexiones
    sock.listen()
    return sock
