#!/bin/bash

# PASO 1: Detectar ruta absoluta del proyecto (sube dos niveles desde /src/bash)
ROOT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"

# PASO 2: Definir archivos de entrada y salida usando rutas absolutas
input_file="$ROOT_DIR/data/raw/beer_profile_and_ratings.csv"
output_file="$ROOT_DIR/data/clean/beer_profile_and_ratings.csv"

# PASO 3: Crear carpeta de salida si no existe
mkdir -p "$(dirname "$output_file")"

# PASO 4: Verificar que el archivo existe
if [[ ! -f "$input_file" ]]; then
    echo "❌ ERROR: Archivo no encontrado: $input_file"
    exit 1
fi

# PASO 5: Limpiar el archivo
gawk '{
    gsub(/"/, "")        # quitar comillas
    gsub(/,/, ";;")      # reemplazar comas
    $0 = tolower($0)     # convertir a minúsculas
    gsub(/;;/, "|")      # convertir ;; en |
    gsub(/[áàäâãå]/, "a")
    gsub(/[éèëê]/, "e")
    gsub(/[íìïî]/, "i")
    gsub(/[óòöôõ]/, "o")
    gsub(/[úùüû]/, "u")
    gsub(/[ç]/, "c")
    gsub(/[ñ]/, "n")
    gsub(/[žźż]/, "z")
    gsub(/[^a-z |]/, "") # quitar todo lo que no sea letras, espacio o |
    print
}' "$input_file" > "$output_file"

# PASO 6: Confirmación
echo "✅ Archivo limpio guardado en: $output_file"
