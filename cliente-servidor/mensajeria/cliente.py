import socket
import threading

HOST = "127.0.0.1"
PORT = 8000


def recibir_mensaje(conexion):
    while True:
        try:
            datos = conexion.recv(1024)

            if not datos:
                print("\nSe perdio conexion")
                break

            print(f"\nMensaje: {datos.decode()}")
            print(">", end="", flush=True)

        except ConnectionResetError:
            print("Conexion terminada")
            break


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
    cliente.connect((HOST, PORT))

    print("Conectado al servidor")

    nombre = input("Tu nombre: ")

    print("Escribe, mesaje. Usa '0' para salir")

    hilo = threading.Thread(target=recibir_mensaje, args=(cliente,), daemon=True)

    hilo.start()

    while True:
        texto = input("> ")

        if texto == "0":
            break

        cliente.sendall(f"[{nombre}]: {texto}".encode())