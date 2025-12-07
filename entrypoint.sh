#!/bin/bash
set -e

REPO_URL="https://github.com/Lucifirius/Prograde-Bot.git"
BRANCH="main"
TMP_DIR="/tmp/prograde-repo"

echo "Updating code from $REPO_URL (branch: $BRANCH)..."

rm -rf "$TMP_DIR"
mkdir -p "$TMP_DIR"

if [ -d "/app/.git" ]; then
    echo "Existing repository found → pulling latest changes"
    cd /app
    git fetch --all
    git reset --hard "origin/$BRANCH"
    # This line is fixed: never delete the mounted prograde_files folder
    git clean -fd -e prograde_files/
else
    echo "No repository found → cloning fresh"
    git clone --branch "$BRANCH" --single-branch "$REPO_URL" "$TMP_DIR"
    cp -a "$TMP_DIR"/. /app/
    rm -rf "$TMP_DIR"
fi

echo "Code is up to date! Starting bot..."
exec "$@"