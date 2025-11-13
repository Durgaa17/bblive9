import requests
from bs4 import BeautifulSoup
import json
import sys
from datetime import datetime
from urllib.parse import quote

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
                direct_url = ""
                
                if 'twitch.tv' in src:
                    platform = "Twitch"
                    # Extract channel name from Twitch URL
                    if 'channel=' in src:
                        channel = src.split('channel=')[1].split('&')[0]
                    elif 'twitch.tv/' in src:
                        channel = src.split('twitch.tv/')[1].split('?')[0].split('/')[0]
                    # Direct Twitch URL for OTT players
                    direct_url = f"https://www.twitch.tv/{channel}"
                    
                elif 'ok.ru' in src:
                    platform = "OK.ru"
                    # Use web player fallback for OK.ru
                    direct_url = f"https://durgaa17.github.io/bblive9/player.html?stream={idx}"
                    
                elif 'youtube.com' in src or 'youtu.be' in src:
                    platform = "YouTube"
                    direct_url = f"https://durgaa17.github.io/bblive9/player.html?stream={idx}"
                    
                elif 'dailymotion.com' in src:
                    platform = "Dailymotion"
                    direct_url = f"https://durgaa17.github.io/bblive9/player.html?stream={idx}"
                else:
                    # Default fallback to web player
                    platform = "Web"
                    direct_url = f"https://durgaa17.github.io/bblive9/player.html?stream={idx}"
                
                source_data = {
                    "id": idx,
                    "name": f"Bigg Boss Stream {idx}",
                    "url": src,
                    "platform": platform,
                    "channel": channel,
                    "embed_url": src,
                    "direct_url": direct_url,
                    "tvg_id": f"BiggBoss{idx}",
                    "tvg_name": f"Bigg Boss Stream {idx}",
                    "group_title": "Bigg Boss Tamil"
                }
                sources.append(source_data)
        
        return sources
        
    except Exception as e:
        print(f"Error scraping: {e}")
        return []

def generate_m3u_playlist(sources, use_direct_links=True):
    """Generate M3U playlist with proper OTT player formatting"""
    m3u_content = ["#EXTM3U"]
    
    for stream in sources:
        # EXTINF line with metadata for OTT players
        extinf_line = f'#EXTINF:-1 tvg-id="{stream["tvg_id"]}" tvg-name="{stream["tvg_name"]}" group-title="{stream["group_title"]}"'
        
        # Add logo if available
        if stream["platform"] == "Twitch":
            extinf_line += ' tvg-logo="https://static-cdn.jtvnw.net/ttv-static/404_boxart.jpg"'
        elif stream["platform"] == "OK.ru":
            extinf_line += ' tvg-logo="https://durgaa17.github.io/bblive9/okru-logo.png"'
        
        extinf_line += f',{stream["name"]} ({stream["platform"]})'
        
        # Choose URL based on preference
        if use_direct_links and stream["direct_url"]:
            stream_url = stream["direct_url"]
        else:
            stream_url = stream["url"]
        
        m3u_content.append(extinf_line)
        m3u_content.append(stream_url)
    
    return "\n".join(m3u_content)

if __name__ == "__main__":
    sources = get_bigg_boss_sources()
    
    # Create output data
    output = {
        "last_updated": datetime.utcnow().isoformat() + "Z",
        "sources": sources,
        "total_sources": len(sources),
        "status": "success"
    }
    
    # Write JSON data
    with open('streams.json', 'w') as f:
        json.dump(output, f, indent=2)
    
    # Generate M3U playlists
    m3u_direct = generate_m3u_playlist(sources, use_direct_links=True)
    m3u_web = generate_m3u_playlist(sources, use_direct_links=False)
    
    # Write M3U files
    with open('playlist.m3u', 'w') as f:
        f.write(m3u_direct)
    
    with open('playlist_web.m3u', 'w') as f:
        f.write(m3u_web)
    
    print(f"Found {len(sources)} streams")
    print("Data written to streams.json")
    print("M3U playlists generated: playlist.m3u, playlist_web.m3u")
