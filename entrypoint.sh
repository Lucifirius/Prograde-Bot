#!/bin/bash
set -e

echo "Ensuring latest code from GitHub..."

if [ -d ".git" ]; then
    echo "Git repository found → pulling latest changes"
    git fetch --all
    git reset --hard origin/main   # or origin/master
    git clean -fd
else
    echo "No git repository found → cloning fresh"
    git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git /tmp/repo
    cp -r /tmp/repo/* /app/
    cp -r /tmp/repo/.git /app/
    rm -rf /tmp/repo
fi

echo "Code is up to date! Starting bot..."
exec "$@"