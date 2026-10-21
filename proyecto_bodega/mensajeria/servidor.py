# Servidor principal de chat para la bodega con soporte multihilo y lectura segura
import socket
import threading
from datetime import datetime
from mensajeria.conexion import crear_socket_servidor
from mensajeria.protocolo import codificar_mensaje, decodificar_mensaje
from mensajeria.persistencia import guardar_en_bitacora

# Diccionario para llevar el control de quién está conectado actualmente
clientes_conectados = {}
bloqueo_hilos = threading.Lock()

def recibir_paquete(conn):
    """Función auxiliar para leer siempre respetando el tamaño exacto (Framing)"""
    try:
        cabecera = conn.recv(4)
        if not cabecera or len(cabecera) < 4:
            return None
        longitud = int.from_bytes(cabecera, byteorder='big')
        cuerpo = conn.recv(longitud)
        if not cuerpo or len(cuerpo) < longitud:
            return None
        return decodificar_mensaje(cuerpo)
    except:
        return None

def manejar_cliente(conn, addr):
    nombre_usuario = None
    try:
        # Recibimos el primer mensaje de autenticación respetando el framing
        mensaje_inicial = recibir_paquete(conn)
        if not mensaje_inicial:
            conn.close()
            return
        
        nombre_usuario = mensaje_inicial.get("remitente")

        with bloqueo_hilos:
            if not nombre_usuario or nombre_usuario in clientes_conectados:
                # Si el nombre ya está ocupado, avisamos y cerramos
                conn.sendall(codificar_mensaje({"tipo": "error", "contenido": "El nombre ya está en uso o es inválido."}))
                conn.close()
                return
            # Registramos al usuario como activo
            clientes_conectados[nombre_usuario] = conn
        
        print(f"[SERVIDOR] ¡El operario {nombre_usuario} se ha conectado desde {addr}!")

        # Bucle para recibir los mensajes posteriores de este cliente
        while True:
            paquete = recibir_paquete(conn)
            if not paquete:
                break
            
            texto = paquete.get("contenido", "")
            canal = paquete.get("canal", "#general")

            # El servidor asigna la autoría real y la hora exacta (Requerimiento clave)
            mensaje_procesado = {
                "remitente": nombre_usuario,
                "canal": canal,
                "contenido": texto,
                "hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            # Guardamos el mensaje en el archivo de bitácora en disco
            guardar_en_bitacora(mensaje_procesado)

            # Reenviamos el mensaje a todos los usuarios conectados
            with bloqueo_hilos:
                paquete_bytes = codificar_mensaje(mensaje_procesado)
                for usuario, socket_cli in clientes_conectados.items():
                    try:
                        socket_cli.sendall(paquete_bytes)
                    except:
                        pass
    except Exception as e:
        print(f"[SERVIDOR] Error con el usuario {nombre_usuario}: {e}")
    finally:
        # Al desconectarse, eliminamos al usuario del registro activo
        if nombre_usuario:
            with bloqueo_hilos:
                if nombre_usuario in clientes_conectados:
                    del clientes_conectados[nombre_usuario]
            print(f"[SERVIDOR] El operario {nombre_usuario} se ha desconectado.")
        conn.close()

def iniciar_servidor():
    servidor = crear_socket_servidor('127.0.0.1', 8000)
    print("[SERVIDOR] Servidor de la bodega iniciado en el puerto 8000...")
    try:
        while True:
            conn, addr = servidor.accept()
            # Creamos un hilo independiente por cada cliente para atenderlos al mismo tiempo
            hilo = threading.Thread(target=manejar_cliente, args=(conn, addr), daemon=True)
            hilo.start()
    except KeyboardInterrupt:
        print("\n[SERVIDOR] Apagando el servidor...")
    finally:
        servidor.close()

if __name__ == "__main__":
    iniciar_servidor()
