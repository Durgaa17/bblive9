# bblive9
making bigg boss season 9 live stream example that get some source from internet.

# Bigg Boss Tamil Season 9 Live Streams

A web application that automatically updates and displays live stream links for Bigg Boss Tamil Season 9.

## Features

- 🤖 **Auto-updating**: Stream links updated every 6 hours via GitHub Actions
- 📱 **Responsive Design**: Works on desktop and mobile devices
- 🔄 **Live Detection**: Automatically detects Twitch, OK.ru, and other platforms
- 🎯 **Direct Links**: Provides direct links to stream sources
- ⚡ **Fast Loading**: Lightweight and fast-loading interface

## How It Works

1. **Scraping**: Python script scrapes the source website for stream links
2. **Automation**: GitHub Actions runs every 6 hours to update links
3. **Frontend**: Beautiful web interface displays the streams
4. **Auto-refresh**: Page automatically checks for new links every 30 minutes

## Local Development

```bash
# Install dependencies
pip install requests beautifulsoup4

# Run scraper manually
python3 scraper.py

# View the website
open index.html
