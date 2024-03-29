#!/bin/bash

# Función para mostrar un mensaje de error y salir del script
mostrar_error() {
    echo "Error: $1"
    exit 1
}

# Función para convertir el tamaño del archivo a MB o GB
convertir_tamaño() {
    local -i size=$1
    if ((size < 1024)); then
        echo "${size}B"
    elif ((size < 1048576)); then
        echo "$((size / 1024))KB"
    elif ((size < 1073741824)); then
        echo "$((size / 1048576))MB"
    else
        echo "$((size / 1073741824))GB"
    fi
}

# Solicitar al usuario la cantidad de MB de los archivos grandes
echo "Ingrese la cantidad de MB que deben tener los archivos grandes:"
read cantidad_mb

# Verificar si la entrada del usuario es un número válido
if ! [[ "$cantidad_mb" =~ ^[0-9]+$ ]]; then
    mostrar_error "La cantidad ingresada no es un número válido."
fi

# Solicitar al usuario el directorio a analizar
echo "Ingrese el directorio a analizar:"
read directorio

# Verificar si el directorio especificado existe y es un directorio
if [ ! -d "$directorio" ]; then
    mostrar_error "El directorio especificado no existe."
fi

# Listar archivos en el directorio y mostrar los archivos más grandes
result=$(find "$directorio" -type f -size +${cantidad_mb}M)

# Guardar la salida en un archivo JSON
output_json="./resources/propetarios.json"
echo "[" > "$output_json"
first=true
while IFS= read -r file; do
    owner=$(stat -c '%U' "$file")
    size=$(stat -c '%s' "$file")
    size_human=$(convertir_tamaño "$size")
    if [ "$first" = false ]; then
        echo "," >> "$output_json"
    fi
    echo "{ \"archivo\": \"$file\", \"propietario\": \"$owner\", \"tamaño\": \"$size_human\" }" >> "$output_json"
    first=false
done <<< "$result"
echo "]" >> "$output_json"

# Guardar la salida en un archivo de texto (TXT)
output_txt="./resources/archivos_mas_grandes.txt"
echo "Los archivos mayores a $cantidad_mb MB en $directorio son:" > "$output_txt"
while IFS= read -r file; do
    size=$(stat -c '%s' "$file")
    type=$(file -b --mime-type "$file")
    size_human=$(convertir_tamaño "$size")
    echo "Archivo: $file - Propietario: $(stat -c '%U' "$file") - Tamaño: $size_human - Tipo: $type" >> "$output_txt"
done <<< "$result"

echo "La información se ha guardado en $output_json (JSON) y $output_txt (TXT)"

