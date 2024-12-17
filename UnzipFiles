#!/bin/bash

backup_file="../TopStordata/TopStor_backup.zip"
password="Ahmed1234"
destination_dir="./"

if [ ! -f "$backup_file" ]; then
    echo "Backup file $backup_file does not exist. Exiting."
    exit 1
fi

unzip -P "$password" "$backup_file" -d "$destination_dir"

if [ $? -eq 0 ]; then
    echo "Backup successfully extracted into $destination_dir"
else
    echo "An error occurred during the extraction process."
fi

