#!/bin/bash

# ✅ Ruta absoluta al directorio donde está este script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# ✅ Rutas relativas al script (no a la terminal)
input_dir="$SCRIPT_DIR/../../data/raw"
output_dir="$SCRIPT_DIR/../../data/clean"


# Crear la carpeta de salida si no existe
mkdir -p "$output_dir"

# Procesar cada archivo CSV en el directorio de entrada
for input_file in "$input_dir"/*.csv; do
    # Extraer el nombre del archivo
    file_name="$(basename "$input_file")"

    # Definir la ruta de salida
    output_file="$output_dir/$file_name"

    # Procesar el archivo
    gawk '{
        # Convertir a minúsculas
        $0 = tolower($0)

        # Reemplazar letras con tilde por sus equivalentes
        gsub(/[áàäâãå]/, "a")
        gsub(/[éèëê]/, "e")
        gsub(/[íìïî]/, "i")
        gsub(/[óòöôõ]/, "o")
        gsub(/[úùüû]/, "u")
        gsub(/[ç]/, "c")
        gsub(/[ñ]/, "n")
        gsub(/[žźż]/, "z")

        # Imprimir la línea limpia
        print
    }' "$input_file" > "$output_file"

    echo "✅ Procesado: $input_file → $output_file"
done
