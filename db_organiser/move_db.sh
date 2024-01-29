#! /bin/bash

# Ensure the destination directory exists
mkdir -p /home/pudrunui/Documents/Database/expenses

# to copy (all .db files)
# Use rsync to copy files with the .db extension to the desired destination directory
# rsync -av home/Documents/Homestay_apps/*.db*.db /home/pudrunui/Documents/Database/expenses

# to move (all .db files)
# Move files with the .db extension to the destination directory
# mv home/Documents/Homestay_apps/*.db /home/pudrunui/Documents/Database/expenses

# Display the file tree of the destination directory
tree /home/pudrunui/Documents/Database/expenses
