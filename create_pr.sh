#!/bin/bash

# Navigate to the project directory
cd "$(dirname "$0")"

# Create a new branch
git checkout -b feature/console-buffering-improvements

# Add the modified files
git add rich/console.py tests/test_console_buffering_improvements.py pull_request.md

# Commit the changes
git commit -m "Add console buffering improvements"

# Push the branch to the remote repository
git push origin feature/console-buffering-improvements

echo "Pull request branch created and pushed successfully!"
echo "You can now create a pull request on GitHub." 