#!/bin/bash

# Bigg Boss Live Stream Updater - Version 3.0
set -e

echo "=== Bigg Boss Live Stream Update Started ==="
date

# Configure git
git config --global user.name "GitHub Actions"
git config --global user.email "actions@github.com"

# Run the Python scraper
echo "Running Python scraper..."
python3 scraper.py

# Check if files were created
if [ ! -f "streams.json" ]; then
    echo "Error: streams.json was not created!"
    exit 1
fi

if [ ! -f "playlist.m3u" ]; then
    echo "Error: playlist.m3u was not created!"
    exit 1
fi

# Add and commit changes
echo "Committing changes to repository..."
git add streams.json playlist.m3u playlist_web.m3u
git commit -m "Version 3.0 - Update streams and M3U playlists - $(date +'%Y-%m-%d %H:%M:%S')" || echo "No changes to commit"

# Push changes
echo "Pushing changes to repository..."
git push

echo "=== Version 3.0 Update Completed Successfully ==="
echo "M3U Playlists:"
echo "- https://durgaa17.github.io/bblive9/playlist.m3u"
echo "- https://durgaa17.github.io/bblive9/playlist_web.m3u"
