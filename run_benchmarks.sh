#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <tag>"
    exit 1
fi

TAG=$1
HASHFILE="asvhashfile"

echo -n -e "\n$TAG" >> "$HASHFILE"

asv run HASHFILE:$HASHFILE

asv publish
