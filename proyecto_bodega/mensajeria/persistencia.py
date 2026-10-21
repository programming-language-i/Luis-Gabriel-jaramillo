# Módulo para guardar los mensajes en un archivo de disco (Bitácora auditable)
import json
from pathlib import Path

def guardar_en_bitacora(mensaje_dict: dict, ruta_archivo: str = "bitacora.jsonl"):
    # Abrimos el archivo en modo de adición ('a') con codificación UTF-8
    with open(ruta_archivo, "a", encoding="utf-8") as f:
        # Guardamos cada mensaje como una línea de texto JSON
        f.write(json.dumps(mensaje_dict, ensure_ascii=False) + "\n")
