#!/bin/bash
# entrypoint.sh - Always update from git when container starts

set -e

echo "Fetching latest code from GitHub..."
git fetch origin

# Reset any local changes (in case you mounted volume with old files)
git reset --hard
git clean -fd

# Switch to your branch (main/master)
git checkout main  # or master, depending on your default branch
git pull origin main

echo "Code updated! Starting bot..."
exec "$@"
