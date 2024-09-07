#!/bin/bash

cd ~/obsidian-vault || exit


if git status --porcelain | grep -q '^[ MADRCU?]'; then
    echo "Changes detected. Pushing to remote repository..."
    git add .
    current_date_time=$(date '+%Y-%m-%d %H:%M:%S')
    git commit -m "${current_date_time} obsidian vault update"
    git push origin main
    echo "Changes pushed successfully."

elif [ "$(git cherry -v)" ]; then
    echo "Unpushed commits detected. Pushing to remote repository..."
    git push origin main
    echo "Unpushed commits pushed successfully."

else
    echo "No changes detected. Nothing to push."
fi

