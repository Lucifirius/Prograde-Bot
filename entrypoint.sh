#!/bin/bash
set -e

REPO_URL="${GIT_REPO_URL:-https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git}"
BRANCH="${GIT_BRANCH:-main}"

echo "Updating code from $REPO_URL (branch: $BRANCH)..."

if [ -d ".git" ]; then
    echo "Existing repo found → pulling latest"
    git fetch --all
    git reset --hard "origin/$BRANCH"
    git clean -fd
else
    echo "No repo found → cloning fresh"
    git clone --branch "$BRANCH" --single-branch "$REPO_URL" /tmp/repo
    rsync -av /tmp/repo/ /app/
    rm -rf /tmp/repo
fi

echo "Code updated! Starting bot..."
exec "$@"