# Pruebas sencillas para verificar que todo funcione correctamente
import unittest
from mensajeria.protocolo import codificar_mensaje, decodificar_mensaje

class TestProyectoBodega(unittest.TestCase):

    def test_codificacion_y_decodificacion(self):
        # Probamos que el mensaje se convierta a bytes y regrese exactamente igual
        datos_originales = {"remitente": "Operario1", "contenido": "Pedido listo"}
        bytes_datos = codificar_mensaje(datos_originales)
        resultado = decodificar_mensaje(bytes_datos[4:]) # Omitimos los 4 bytes del prefijo
        self.assertEqual(datos_originales, resultado)

if __name__ == "__main__":
    unittest.main()
