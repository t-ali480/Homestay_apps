#!/bin/bash

# Directory and file paths
f_name="expenses.db"
target_file="/home/pudrunui/Documents/Database/expenses/$f_name"

# Check if the file is the target of a symlink
if [ -L "$target_file" ]; then
    source_file=$(readlink -f "$target_file")
    echo "$target_file is the target of a symlink."
    echo "Symlink pointing to: $source_file"
    
    # Identify the source of the symlink
    if [ -e "$source_file" ]; then
        echo "Source of the symlink: $source_file"
    else
        echo "Source file does not exist: $source_file"
    fi
else
    echo "$target_file is not the target of a symlink."
fi
