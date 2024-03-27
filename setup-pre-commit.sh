#!/bin/bash

# Stop the script if any command fails
set -e

run_command() {
    echo "Running command: $1"
    $1
}

echo "Installing pre-commit..."
run_command "pip install pre-commit"

echo "Setting up pre-commit hooks..."
run_command "pre-commit install"

echo "Setup complete."
