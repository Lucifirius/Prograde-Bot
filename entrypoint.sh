#!/bin/bash
set -e

REPO_URL="https://github.com/Lucifirius/Prograde-Bot.git"
BRANCH="main"

echo "Updating code from GitHub..."

if [ -d "/app/.git" ]; then
    echo "Pulling latest changes..."
    cd /app
    git fetch --all
    git reset --hard "origin/$BRANCH"
    git clean -fd -e prograde_files/ -e .env
else
    echo "First time setup — cloning repo into current folder..."
    git clone --branch "$BRANCH" --single-branch "$REPO_URL" /tmp/temp-repo
    cp -r /tmp/temp-repo/* /app/
    cp -r /tmp/temp-repo/.git /app/
    rm -rf /tmp/temp-repo
fi

echo "Code ready! Starting bot..."
exec "$@"