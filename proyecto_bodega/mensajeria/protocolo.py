# Módulo para empaquetar y desempaquetar los mensajes usando formato JSON y bytes (Framing)
import json

def codificar_mensaje(diccionario: dict) -> bytes:
    # Convertimos el mensaje a formato de texto JSON
    texto_json = json.dumps(diccionario, ensure_ascii=False)
    bytes_cuerpo = texto_json.encode('utf-8')
    
    # Agregamos un prefijo de 4 bytes que indica el tamaño exacto del mensaje (Framing)
    longitud = len(bytes_cuerpo)
    return longitud.to_bytes(4, byteorder='big') + bytes_cuerpo

def decodificar_mensaje(bytes_datos: bytes) -> dict:
    # Convertimos los bytes recibidos de la red nuevamente a un diccionario de Python
    texto_json = bytes_datos.decode('utf-8')
    return json.loads(texto_json)
