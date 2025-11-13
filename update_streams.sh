#!/bin/bash

# Bigg Boss Live Stream Updater - Version 2.0
set -e

echo "=== Bigg Boss Live Stream Update Started ==="
date

# Configure git
git config --global user.name "GitHub Actions"
git config --global user.email "actions@github.com"

# Run the Python scraper
echo "Running Python scraper..."
python3 scraper.py

# Check if streams.json was created
if [ ! -f "streams.json" ]; then
    echo "Error: streams.json was not created!"
    exit 1
fi

# Add and commit changes
echo "Committing changes to repository..."
git add streams.json
git commit -m "Update stream links - $(date +'%Y-%m-%d %H:%M:%S')" || echo "No changes to commit"

# Push changes
echo "Pushing changes to repository..."
git push

echo "=== Update Completed Successfully ==="
