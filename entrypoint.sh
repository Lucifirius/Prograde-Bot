#!/bin/bash
set -e

REPO_URL="https://github.com/Lucifirius/Prograde-Bot.git"
BRANCH="main"
TMP_DIR="/tmp/prograde-repo"

echo "Updating code from $REPO_URL (branch: $BRANCH)..."

# Always start clean
rm -rf "$TMP_DIR"
mkdir -p "$TMP_DIR"

if [ -d "/app/.git" ]; then
    echo "Existing repository found → pulling latest changes"
    cd /app
    git fetch --all
    git reset --hard "origin/$BRANCH"
    git clean -fd
else
    echo "No repository found → cloning fresh"
    git clone --branch "$BRANCH" --single-branch "$REPO_URL" "$TMP_DIR"

    # Simple cp method (works everywhere, no rsync needed)
    cp -a "$TMP_DIR"/. /app/

    # Clean up
    rm -rf "$TMP_DIR"
fi

echo "Code is up to date! Starting bot..."
exec "$@"