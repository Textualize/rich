#!/bin/bash

# Stop the script if any command fails
set -e

run_command() {
    echo "Running command: $1"
    $1
}

echo "Installing Poetry..."
run_command "pip install poetry"

echo "Installing project dependencies with Poetry..."
run_command "poetry install"

echo "Installing pre-commit..."
run_command "poetry run pip install pre-commit"

echo "Setting up pre-commit hooks..."
run_command "poetry run pre-commit install"

echo "Setup complete."
