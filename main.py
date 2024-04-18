#!/usr/bin/env python3
import os
from scripts.file_manager import FileManager
from scripts.path_converter import convert_windows_path

def main():
    directory = input("Ingrese la ruta del directorio a analizar: ")
    
    # Verificar el sistema operativo
    if os.name == 'nt':  # Windows
        directory = convert_windows_path(directory)
    else:  # Linux
        directory = directory
    
    # Crear instancia de FileManager
    file_manager = FileManager(directory)
    
    # Resto de la lógica...
    # file_manager.execute(cant_mb)
    file_manager = FileManager(directory)
    cantidad_mb = int(input("Ingrese la cantidad de MB que deben tener los archivos grandes que usted considera: "))
    file_manager.execute(cantidad_mb)

if __name__ == "__main__":
    main()

