#!/bin/bash
set -e

# 1. If called with NO arguments, run ALL tests
if [ -z "$1" ]; then
    echo "Running all tests..."
    pytest
# 2. If called WITH comma-separated paths, run ONLY those files
else
    echo "Parsing test files..."
    TARGET_TESTS=$(echo "$1" | tr ',' ' ')
    echo "Running tests for: $TARGET_TESTS"
    pytest $TARGET_TESTS
fi