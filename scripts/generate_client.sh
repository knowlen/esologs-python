#!/bin/bash
# Wrapper script for generating GraphQL client with proper file organization

echo "Generating GraphQL client..."

# Activate virtual environment if not already active
if [[ -z "$VIRTUAL_ENV" ]]; then
    source venv/bin/activate
fi

# Run ariadne-codegen
echo "Running ariadne-codegen..."
ariadne-codegen client --config mini.toml

# Move generated files to _generated subdirectory
echo "Organizing generated files..."
python scripts/post_codegen.py

echo "Done! Generated files are in esologs/_generated/"
