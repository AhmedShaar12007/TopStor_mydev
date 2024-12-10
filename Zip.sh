#!/bin/bash

# Variables
destination_dir="/TopStordata"
zip_filename="TopStor_backup.zip"
password="Ahmed1234"  

directories=("TopStor" "pace" "topstorweb")

# Ensure the destination directory exists
if [ ! -d "$destination_dir" ]; then
    echo "Creating destination directory: $destination_dir"
    mkdir -p "$destination_dir"
fi

# Check if all directories exist
for dir in "${directories[@]}"; do
    if [ ! -d "$dir" ]; then
        echo "Directory $dir does not exist. Exiting."
        exit 1
    fi
done

# Create a zip file with a password
zip -r -P "$password" "$destination_dir/$zip_filename" "${directories[@]}"

if [ $? -eq 0 ]; then
    echo "Directories successfully compressed into $destination_dir/$zip_filename"
else
    echo "An error occurred during the compression process."
fi

