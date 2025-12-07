#!/bin/bash
set -e

REPO_URL="https://github.com/Lucifirius/Prograde-Bot.git"
BRANCH="main"
TMP_DIR="/tmp/repo"

echo "Updating code from $REPO_URL (branch: $BRANCH)..."

# Always clean any leftover temp dir first
rm -rf "$TMP_DIR"

if [ -d ".git" ]; then
    echo "Existing repository found → pulling latest changes"
    git fetch --all
    git reset --hard "origin/$BRANCH"
    git clean -fd
else
    echo "No repository found → cloning fresh"
    git clone --branch "$BRANCH" --single-branch "$REPO_URL" "$TMP_DIR"
    rsync -av --remove-source-files "$TMP_DIR"/ /app/
    rm -rf "$TMP_DIR"
    # Copy hidden files too (like .git)
    cp -r "$TMP_DIR"/. /app/ 2>/dev/null || true
fi

echo "Code is up to date! Starting bot..."
exec "$@"