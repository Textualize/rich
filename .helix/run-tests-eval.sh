#!/usr/bin/env bash

set -e

if [ $# -eq 0 ]; then
    pytest
else
    IFS=',' read -ra TESTFILES <<< "$1"
    pytest "${TESTFILES[@]}"
fi