#!/usr/bin/env python3
import os
import sys
import json
from subprocess import check_output

# Función para mostrar un mensaje de error y salir del script
def mostrar_error(msg):
    print("Error:", msg, file=sys.stderr)
    sys.exit(1)

# Función para convertir el tamaño del archivo a MB o GB
def convertir_tamaño(size):
    size = int(size)
    if size < 1024:
        return f"{size}B"
    elif size < 1048576:
        return f"{size // 1024}KB"
    elif size < 1073741824:
        return f"{size // 1048576}MB"
    else:
        return f"{size // 1073741824}GB"

# Solicitar al usuario el directorio
directorio = input("Ingrese la ruta del directorio a analizar: ")

# Verificar si el directorio especificado existe y es un directorio
if not os.path.isdir(directorio):
    mostrar_error("El directorio especificado no existe o no es un directorio.")

# Solicitar al usuario la cantidad de MB de los archivos grandes
try:
    cantidad_mb = int(input("Ingrese la cantidad de MB que deben tener los archivos grandes que usted considera son grandes: "))
except ValueError:
    mostrar_error("La cantidad ingresada no es un número válido.")

# Definir las rutas de los archivos de salida
output_dir = "./resources"
output_json = os.path.join(output_dir, "propietarios.json")
output_txt = os.path.join(output_dir, "archivos_mas_grandes.txt")

# Verificar si los archivos de salida existen y preguntar al usuario si desea sobrescribirlos
if os.path.exists(output_json) or os.path.exists(output_txt):
    respuesta = input("Los archivos de salida ya existen. ¿Desea sobrescribirlos? (s/n): ").strip().lower()
    if respuesta != "s":
        mostrar_error("Operación cancelada por el usuario.")

# Listar archivos en el directorio y mostrar los archivos más grandes
try:
    result = check_output(["find", directorio, "-type", "f", "-size", f"+{cantidad_mb}M"]).decode("utf-8").splitlines()
except Exception as e:
    mostrar_error(f"No se pudo listar los archivos: {e}")

# Verificar si se encontraron archivos
if not result:
    mostrar_error(f"No se encontraron archivos mayores a {cantidad_mb}MB en el directorio: {directorio}")

# Crear lista de diccionarios para el JSON
output_json_data = []
for file in result:
    # Obtener la parte del servidor
    servidor = file.split("server=")[-1].split(",")[0]
    # Obtener la parte del directorio después de la conexión
    directorio_sin_conexion = file.split("smb-share:server=")[-1].split(",")[-1][2:]
    # Eliminar el nombre del archivo del directorio
    directorio_sin_archivo = os.path.dirname(directorio_sin_conexion).replace("are=d$", "")
    owner = os.stat(file).st_uid
    size = os.stat(file).st_size
    size_human = convertir_tamaño(size)
    type = check_output(["file", "-b", "--mime-type", file]).decode("utf-8").strip()
    output_json_data.append({
        "archivo": os.path.basename(file),
        "directorio": directorio_sin_archivo,
        "servidor": servidor,
        "propietario": owner,
        "tamaño": size_human,
        "tipo": type
    })

# Guardar la salida en un archivo JSON
try:
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(output_json_data, f, indent=4, ensure_ascii=False)
except Exception as e:
    mostrar_error(f"No se pudo escribir en el archivo JSON: {e}")

# Guardar la salida en un archivo de texto (TXT)
try:
    with open(output_txt, "w") as f:
        f.write(f"Los archivos mayores a {cantidad_mb} MB en {directorio} son:\n")
        for file in result:
            size = os.stat(file).st_size
            size_human = convertir_tamaño(size)
            type = check_output(["file", "-b", "--mime-type", file]).decode("utf-8").strip()
            f.write(f"Archivo: {os.path.basename(file)} - Propietario: {owner} - Tamaño: {size_human} - Tipo: {type}\n")
except Exception as e:
    mostrar_error(f"No se pudo escribir en el archivo TXT: {e}")

print(f"La información se ha guardado en {output_json} (JSON) y {output_txt} (TXT)")





