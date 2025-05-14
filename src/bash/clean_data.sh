#!/bin/bash

# Define input and output directories
input_dir="../../data/raw"
output_dir="../../data/clean"

# Create the output directory if it doesn't exist
mkdir -p "$output_dir"

# Process each CSV file in the input directory
for input_file in "$input_dir"/*.csv; do
    # Extract the file name without the directory
    file_name="$(basename "$input_file")"

    # Define the output file path
    output_file="$output_dir/$file_name"

    # Process the file
    gawk '{
        # Remove quotes
        #gsub(/"/, "")

        # Replace commas with ;;
        #gsub(/,/, ";;")

        # Convert to lowercase
        $0 = tolower($0)

        # Replace ;; with |
        #gsub(/;;/, "|")

        # Replace slavish letters with corresponding English alphabet
        gsub(/[áàäâãå]/, "a")
        gsub(/[éèëê]/, "e")
        gsub(/[íìïî]/, "i")
        gsub(/[óòöôõ]/, "o")
        gsub(/[úùüû]/, "u")
        gsub(/[ç]/, "c")
        gsub(/[ñ]/, "n")
        gsub(/[žźż]/, "z")

        # Remove all characters that are not in the English alphabet, space, or |
        # gsub(/[^a-z |]/, "")

        print
    }' "$input_file" > "$output_file"
    echo "Processed $input_file -> $output_file"
done
