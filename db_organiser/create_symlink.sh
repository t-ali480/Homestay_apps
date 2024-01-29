#!/bin/bash

# Directory and file paths
source_dir="/home/pudrunui/Documents/Homestay_apps/db_list"
target_dir="/home/pudrunui/Documents/Database/expenses"
file_name="expenses.db"

# Ensure the source file exists
if [ -e "$source_dir/$file_name" ]; then
    # Create a symbolic link from the source to the target
    ln -s "$source_dir/$file_name" "$target_dir/$file_name"
    echo "Symlink created: $target_dir/$file_name -> $source_dir/$file_name"
else
    echo "Error: Source file $source_dir/$file_name not found."
fi


# create symlink