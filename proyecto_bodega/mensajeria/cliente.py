# Aplicación de cliente para que los operarios envíen y reciban mensajes
import socket
import threading
from mensajeria.protocolo import codificar_mensaje, decodificar_mensaje

def escuchar_mensajes(sock):
    # Hilo secundario para recibir los mensajes del servidor en tiempo real
    try:
        while True:
            cabecera = sock.recv(4)
            if not cabecera:
                break
            longitud = int.from_bytes(cabecera, byteorder='big')
            cuerpo = sock.recv(longitud)
            if not cuerpo:
                break
            
            msg = decodificar_mensaje(cuerpo)
            print(f"\n[{msg.get('canal', '#general')}] {msg.get('hora')} - {msg.get('remitente')}: {msg.get('contenido')}\nTú > ", end="", flush=True)
    except:
        pass

def iniciar_cliente():
    nombre = input("Escribe tu nombre de usuario: ").strip()
    if not nombre:
        print("El nombre no puede estar vacío.")
        return

    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        cliente.connect(('127.0.0.1', 8000))
    except ConnectionRefusedError:
        print("[CLIENTE] No se pudo conectar al servidor. Asegúrate de que esté encendido.")
        return

    # Enviamos el nombre inicial para registrarnos en el servidor
    cliente.sendall(codificar_mensaje({"remitente": nombre, "contenido": "CONEXION"}))

    # Lanzamos el hilo de escucha
    hilo = threading.Thread(target=escuchar_mensajes, args=(cliente,), daemon=True)
    hilo.start()

    print("\n[CLIENTE] ¡Conectado al chat de la bodega! Escribe tus mensajes (o escribe 'salir' para terminar):")
    try:
        while True:
            texto = input("Tú > ")
            if texto.lower() == 'salir':
                break
            if texto.strip():
                paquete = {
                    "remitente": nombre,
                    "canal": "#general",
                    "contenido": texto
                }
                cliente.sendall(codificar_mensaje(paquete))
    finally:
        cliente.close()
        print("[CLIENTE] Sesión finalizada.")

if __name__ == "__main__":
    iniciar_cliente()
