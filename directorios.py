import os
import json

def mostrar_error(mensaje):
    print("Error:", mensaje)
    exit(1)

def convertir_tamaño(size):
    if size < 1024:
        return f"{size}B"
    elif size < 1048576:
        return f"{size // 1024}KB"
    elif size < 1073741824:
        return f"{size // 1048576}MB"
    else:
        return f"{size // 1073741824}GB"

cantidad_mb = input("Ingrese la cantidad de MB que deben tener los archivos grandes: ")

if not cantidad_mb.isdigit():
    mostrar_error("La cantidad ingresada no es un número válido.")

directorio = input("Ingrese el directorio a analizar: ")

if not os.path.isdir(directorio):
    mostrar_error("El directorio especificado no existe.")

result = []
for root, _, files in os.walk(directorio):
    for file in files:
        file_path = os.path.join(root, file)
        size = os.path.getsize(file_path)
        if size > int(cantidad_mb) * 1024 * 1024:
            owner = os.stat(file_path).st_uid
            size_human = convertir_tamaño(size)
            result.append({
                "archivo": file_path,
                "propietario": owner,
                "tamaño": size_human
            })

output_json = "./resources/propetarios.json"
output_txt = "./resources/archivos_mas_grandes.txt"

try:
    with open(output_json, "w") as json_file:
        json.dump(result, json_file, indent=4)
    
    with open(output_txt, "w") as txt_file:
        txt_file.write(f"Los archivos mayores a {cantidad_mb} MB en {directorio} son:\n")
        for item in result:
            txt_file.write(f"Archivo: {item['archivo']} - Propietario: {item['propietario']} - Tamaño: {item['tamaño']} - Tipo: {os.path.splitext(item['archivo'])[1]}\n")

    print(f"La información se ha guardado en {output_json} (JSON) y {output_txt} (TXT)")
except Exception as e:
    mostrar_error(f"Error al guardar los archivos: {e}")
