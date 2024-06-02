#!/bin/bash

# Finds path of the directory containing the file "tree.sh"
script_dir=$(dirname "$(realpath "$0")")

# Change directory to the desired directory
cd "$script_dir" || exit

# Run tree command and save its output to a temporary file
tmpfile=$(mktemp)
tree -L 2 > "$tmpfile"

# Remove the old tree output from the markdown file
sed -i '/<!-- STRUCTURE START -->/,/<!-- STRUCTURE END -->/d' docs/structure.md

# Append the new tree output to the markdown file
cat <<EOT >> docs/structure.md
<!-- STRUCTURE START -->
$(cat "$tmpfile")
<!-- STRUCTURE END  -->
EOT

# Remove the temporary file
rm "$tmpfile"
