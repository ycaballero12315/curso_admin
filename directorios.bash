#!/bin/bash

# Función para mostrar un mensaje de error y salir del script
mostrar_error() {
    echo "Error: $1" >&2
    exit 1
}

# Función para convertir el tamaño del archivo a MB o GB
convertir_tamaño() {
    local size="$1"
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

# Verificar si se pasó un directorio como argumento
if [ "$#" -ne 1 ]; then
    mostrar_error "Se requiere un directorio como argumento."
fi

directorio="$1"

# Verificar si el directorio especificado existe y es un directorio
if [ ! -d "$directorio" ]; then
    mostrar_error "El directorio especificado no existe."
fi

# Solicitar al usuario la cantidad de MB de los archivos grandes
echo "Ingrese la cantidad de MB que deben tener los archivos grandes que usted considera son grandes:"
read cantidad_mb

# Verificar si la entrada del usuario es un número válido
if ! [[ "$cantidad_mb" =~ ^[0-9]+$ ]]; then
    mostrar_error "La cantidad ingresada no es un número válido."
fi

# Definir las rutas de los archivos de salida
output_dir="./resources"
output_json="$output_dir/propetarios.json"
output_txt="$output_dir/archivos_mas_grandes.txt"

# Crear directorio de salida si no existe
if ! mkdir -p "$output_dir"; then
    mostrar_error "No se pudo crear el directorio de salida: $output_dir"
fi

# Listar archivos en el directorio y mostrar los archivos más grandes
result=$(find "$directorio" -type f -size +${cantidad_mb}M)

# Verificar si se encontraron archivos
if [ -z "$result" ]; then
    mostrar_error "No se encontraron archivos mayores a ${cantidad_mb}MB en el directorio: $directorio"
fi

# Guardar la salida en un archivo JSON
{
    echo "["
    first=true
    while IFS= read -r file; do
        # Obtener la parte del servidor
        servidor=$(echo "$file" | sed -E 's/.*server=([^,]+),.*/\1/')
        # Obtener la parte del directorio después de la conexión
        directorio_sin_conexion=$(echo "$file" | sed -E 's/.*(smb-share:server=[^,]+,[^\/]*)(.*)/\2/')
        # Eliminar el nombre del archivo del directorio
        directorio_sin_archivo=$(dirname "$directorio_sin_conexion")
        owner=$(stat -c '%U' "$file")
        size=$(stat -c '%s' "$file")
        size_human=$(convertir_tamaño "$size")
        type=$(file -b --mime-type "$file")
        if [ "$first" = false ]; then
            echo ","
        fi
        printf '{"archivo": "%s", "directorio": "%s", "servidor": "%s", "propietario": "%s", "tamaño": "%s", "tipo": "%s"}' \
            "$(basename "$file")" \
            "$directorio_sin_archivo" \
            "$servidor" \
            "$owner" \
            "$size_human" \
            "$type"
        first=false
    done <<< "$result"
    echo "]"
} > "$output_json" || mostrar_error "No se pudo escribir en el archivo JSON: $output_json"

# Guardar la salida en un archivo de texto (TXT)
{
    echo "Los archivos mayores a $cantidad_mb MB en $directorio son:"
    while IFS= read -r file; do
        size=$(stat -c '%s' "$file")
        type=$(file -b --mime-type "$file")
        size_human=$(convertir_tamaño "$size")
        printf "Archivo: %s - Propietario: %s - Tamaño: %s - Tipo: %s\n" "$(basename "$file")" "$(stat -c '%U' "$file")" "$size_human" "$type"
    done <<< "$result"
} > "$output_txt" || mostrar_error "No se pudo escribir en el archivo TXT: $output_txt"

echo "La información se ha guardado en $output_json (JSON) y $output_txt (TXT)"







