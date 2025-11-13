import requests
from bs4 import BeautifulSoup
import json
import sys

def get_bigg_boss_sources():
    url = "https://www.1tamilcrow.net/watch-bigg-boss-tamil-season-9-live-stream/"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        print("Fetching Bigg Boss live stream page...")
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        sources = []
        
        # Extract all iframes
        all_iframes = soup.find_all('iframe')
        
        for idx, iframe in enumerate(all_iframes, 1):
            if iframe.get('src'):
                src = iframe['src']
                # Convert relative URLs to absolute
                if src.startswith('//'):
                    src = 'https:' + src
                
                # Determine platform type
                platform = "Unknown"
                channel = ""
                
                if 'twitch.tv' in src:
                    platform = "Twitch"
                    # Extract channel name from Twitch URL
                    if 'channel=' in src:
                        channel = src.split('channel=')[1].split('&')[0]
                    elif 'twitch.tv/' in src:
                        channel = src.split('twitch.tv/')[1].split('?')[0].split('/')[0]
                elif 'ok.ru' in src:
                    platform = "OK.ru"
                elif 'youtube.com' in src or 'youtu.be' in src:
                    platform = "YouTube"
                elif 'dailymotion.com' in src:
                    platform = "Dailymotion"
                
                source_data = {
                    "id": idx,
                    "name": f"Stream {idx}",
                    "url": src,
                    "platform": platform,
                    "channel": channel,
                    "embed_url": src
                }
                sources.append(source_data)
        
        # Create output data
        output = {
            "last_updated": None,  # Will be set by the workflow
            "sources": sources,
            "total_sources": len(sources),
            "status": "success"
        }
        
        return output
        
    except Exception as e:
        error_output = {
            "last_updated": None,
            "sources": [],
            "total_sources": 0,
            "status": "error",
            "error_message": str(e)
        }
        return error_output

if __name__ == "__main__":
    result = get_bigg_boss_sources()
    
    # Add timestamp
    from datetime import datetime
    result["last_updated"] = datetime.utcnow().isoformat() + "Z"
    
    # Output as JSON
    print(json.dumps(result, indent=2))
    
    # Also write to file
    with open('streams.json', 'w') as f:
        json.dump(result, f, indent=2)
    
    print(f"\nFound {result['total_sources']} streams")
    print("Data written to streams.json")
