#!/usr/bin/env python3
import os
import subprocess
import json

# Función para mostrar un mensaje de error y salir del script
def mostrar_error(msg):
    print(f"Error: {msg}")
    exit(1)

# Función para convertir el tamaño del archivo a MB o GB
def convertir_tamaño(size):
    if size < 1024:
        return f"{size}B"
    elif size < 1048576:
        return f"{size // 1024}KB"
    elif size < 1073741824:
        return f"{size // 1048576}MB"
    else:
        return f"{size // 1073741824}GB"

# Solicitar al usuario la cantidad de MB de los archivos grandes
cantidad_mb = input("Ingrese la cantidad de MB que deben tener los archivos grandes: ")

# Verificar si la entrada del usuario es un número válido
if not cantidad_mb.isdigit():
    mostrar_error("La cantidad ingresada no es un número válido.")

cantidad_mb = int(cantidad_mb)

# Solicitar al usuario el directorio a analizar
directorio = input("Ingrese el directorio a analizar: ")

# Verificar si el directorio especificado existe y es un directorio
if not os.path.isdir(directorio):
    mostrar_error("El directorio especificado no existe.")

# Listar archivos en el directorio y mostrar los archivos más grandes
result = subprocess.check_output(["find", directorio, "-type", "f", "-size", f"+{cantidad_mb}M"]).decode().splitlines()

# Guardar la salida en un archivo JSON
output_json = "./resources/propetarios.json"
with open(output_json, 'w') as f:
    f.write("[")
    first = True
    for file in result:
        owner = os.stat(file).st_uid
        size = os.stat(file).st_size
        size_human = convertir_tamaño(size)
        if not first:
            f.write(",\n")
        f.write(json.dumps({"archivo": file, "propietario": owner, "tamaño": size_human}))
        first = False
    f.write("]")

# Guardar la salida en un archivo de texto (TXT)
output_txt = "./resources/archivos_mas_grandes.txt"
with open(output_txt, 'w') as f:
    f.write(f"Los archivos mayores a {cantidad_mb} MB en {directorio} son:\n")
    for file in result:
        size = os.stat(file).st_size
        file_type = subprocess.check_output(["file", "-b", "--mime-type", file]).decode().strip()
        size_human = convertir_tamaño(size)
        f.write(f"Archivo: {file} - Propietario: {owner} - Tamaño: {size_human} - Tipo: {file_type}\n")

print(f"La información se ha guardado en {output_json} (JSON) y {output_txt} (TXT)")
