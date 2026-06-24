#!/bin/bash
# KSTjiwoo + KSTjiwoo-backup daily git backup script
# Runs via git-bash on Windows

set -e
export HOME=/c/Users/sxeyc
cd /c/Users/sxeyc/KSTjiwoo

# Remove stale lock if exists
rm -f .git/index.lock

# Add all changes
git add -A

# Check if there are staged changes to commit
if git diff --cached --quiet; then
    echo "No changes to commit"
    exit 0
fi

# Commit with timestamp
DATE=$(date +%Y-%m-%d)
git commit -m "auto: daily backup $DATE" || true

# Push to origin
timeout 120 git push origin main 2>&1 || echo "Push to origin failed/timed out"

# Push to backup
timeout 120 git push backup main 2>&1 || echo "Push to backup failed/timed out"

echo "Backup completed: $DATE"
