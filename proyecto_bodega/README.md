# Sistema de Mensajería Interna - Bodega

## Instrucciones para ejecutar:

1. **Abrir la terminal en Visual Studio Code** dentro de la carpeta `proyecto_bodega`.
2. **Iniciar el servidor:**
   ```powershell
   $env:PYTHONPATH="$PWD"
   py -m mensajeria.servidor
   ```
3. **Iniciar un cliente (en otra pestaña de la terminal):**
   ```powershell
   $env:PYTHONPATH="$PWD"
   py -m mensajeria.cliente
   ```
