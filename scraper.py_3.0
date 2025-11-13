import requests
from bs4 import BeautifulSoup
import json
import re
from datetime import datetime, timezone

def get_best_streams():
    """
    Get the best working streams from multiple sources
    """
    streams = []
    
    # Primary sources to check (your provided links)
    sources = [
        {
            'name': 'TamilCrow',
            'url': 'https://www.1tamilcrow.net/watch-bigg-boss-tamil-season-9-live-stream/',
            'priority': 1
        },
        {
            'name': 'Arivumani', 
            'url': 'https://arivumani.net/bigg-boss-season-9-live/',
            'priority': 1
        }
    ]
    
    # Check each source
    for source in sources:
        try:
            print(f"Checking {source['name']}...")
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(source['url'], headers=headers, timeout=15)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            source_streams = extract_streams_from_page(soup, source['name'])
            if source_streams:
                streams.extend(source_streams)
                print(f"  Found {len(source_streams)} streams")
            else:
                print(f"  No streams found")
            
        except Exception as e:
            print(f"  Error with {source['name']}: {e}")
    
    # If no streams found from websites, use fallback streams
    if not streams:
        print("No streams found from websites, using fallback streams...")
        streams = get_fallback_streams()
    
    # Remove duplicates
    unique_streams = remove_duplicate_streams(streams)
    
    # Add TVG metadata to all streams
    for i, stream in enumerate(unique_streams):
        stream['id'] = i + 1
        stream['tvg_id'] = f"BiggBoss{i+1}"
        stream['tvg_name'] = f"Bigg Boss {stream['platform']}"
        stream['group_title'] = "Bigg Boss Tamil S9"
    
    return unique_streams[:8]  # Return top 8 streams max

def get_fallback_streams():
    """Fallback streams in case websites don't work"""
    return [
        {
            'name': "Bigg Boss - Arivumani 1076",
            'url': "https://player.twitch.tv/?channel=arivumani1076&parent=www.1tamilcrow.net",
            'embed_url': "https://player.twitch.tv/?channel=arivumani1076&parent=www.1tamilcrow.net",
            'platform': 'Twitch',
            'channel': 'arivumani1076',
            'direct_url': "https://www.twitch.tv/arivumani1076",
            'type': 'twitch',
            'quality': 'live',
            'source': 'TamilCrow'
        },
        {
            'name': "Bigg Boss - Arivumani 1075", 
            'url': "https://player.twitch.tv/?channel=arivumani1075&parent=www.1tamilcrow.net",
            'embed_url': "https://player.twitch.tv/?channel=arivumani1075&parent=www.1tamilcrow.net",
            'platform': 'Twitch',
            'channel': 'arivumani1075',
            'direct_url': "https://www.twitch.tv/arivumani1075",
            'type': 'twitch',
            'quality': 'live',
            'source': 'TamilCrow'
        },
        {
            'name': "Bigg Boss - OK.ru",
            'url': "https://ok.ru/videoembed/9484647407325?nochat=1",
            'embed_url': "https://ok.ru/videoembed/9484647407325?nochat=1", 
            'platform': 'OK.ru',
            'channel': '',
            'direct_url': "https://durgaa17.github.io/bblive9/player.html?source=okru",
            'type': 'okru',
            'quality': 'adaptive',
            'source': 'TamilCrow'
        }
    ]

def extract_streams_from_page(soup, source_name):
    """
    Extract streams from HTML page
    """
    streams = []
    iframes = soup.find_all('iframe')
    
    for idx, iframe in enumerate(iframes):
        src = iframe.get('src', '')
        if not src:
            continue
            
        # Convert to absolute URL
        if src.startswith('//'):
            src = 'https:' + src
        
        # Detect platform and create stream data
        platform = detect_platform(src)
        channel = extract_channel_info(src, platform)
        
        stream_data = {
            'name': f"Bigg Boss Stream {len(streams) + 1}",
            'url': src,
            'platform': platform,
            'channel': channel,
            'embed_url': src,
            'direct_url': get_direct_url(src, platform, channel),
            'type': 'embedded',
            'quality': 'adaptive',
            'source': source_name
        }
        
        # Customize name based on platform and channel
        if platform == 'Twitch' and channel:
            stream_data['name'] = f"Bigg Boss - {channel}"
        
        streams.append(stream_data)
    
    return streams

def detect_platform(url):
    """Detect streaming platform from URL"""
    url_lower = url.lower()
    
    if 'twitch.tv' in url_lower:
        return 'Twitch'
    elif 'ok.ru' in url_lower:
        return 'OK.ru'
    elif 'youtube.com' in url_lower or 'youtu.be' in url_lower:
        return 'YouTube'
    elif 'dailymotion.com' in url_lower:
        return 'Dailymotion'
    elif 'm3u8' in url_lower:
        return 'HLS'
    else:
        return 'Web'

def extract_channel_info(url, platform):
    """Extract channel name from URL"""
    if platform == 'Twitch':
        if 'channel=' in url:
            return url.split('channel=')[1].split('&')[0]
        elif 'twitch.tv/' in url:
            return url.split('twitch.tv/')[1].split('?')[0].split('/')[0]
    return ""

def get_direct_url(url, platform, channel):
    """Get direct URL for IPTV players"""
    if platform == 'Twitch' and channel:
        return f"https://www.twitch.tv/{channel}"
    elif platform == 'OK.ru':
        return f"https://durgaa17.github.io/bblive9/player.html?source=okru"
    else:
        return url

def remove_duplicate_streams(streams):
    """Remove duplicate streams based on URL"""
    seen_urls = set()
    unique_streams = []
    
    for stream in streams:
        stream_id = stream['url']
        if stream_id not in seen_urls:
            seen_urls.add(stream_id)
            unique_streams.append(stream)
    
    return unique_streams

def generate_m3u_playlist(streams):
    """Generate M3U playlist for IPTV players"""
    m3u_content = ["#EXTM3U"]
    
    for stream in streams:
        # EXTINF line with metadata
        extinf_line = f'#EXTINF:-1 tvg-id="{stream["tvg_id"]}" tvg-name="{stream["tvg_name"]}" group-title="{stream["group_title"]}"'
        
        # Add platform-specific logos
        if stream['platform'] == 'Twitch':
            extinf_line += ' tvg-logo="https://static-cdn.jtvnw.net/ttv-static/404_boxart.jpg"'
        elif stream['platform'] == 'OK.ru':
            extinf_line += ' tvg-logo="https://freelogopng.com/images/all_img/1656500907ok-ru-logo.png"'
        
        extinf_line += f',{stream["name"]} ({stream["platform"]})'
        
        # Use direct URL for IPTV
        stream_url = stream['direct_url']
        
        m3u_content.append(extinf_line)
        m3u_content.append(stream_url)
    
    return "\n".join(m3u_content)

def generate_web_m3u_playlist(streams):
    """Generate M3U playlist with web player fallbacks"""
    m3u_content = ["#EXTM3U"]
    
    for stream in streams:
        extinf_line = f'#EXTINF:-1 tvg-id="{stream["tvg_id"]}" tvg-name="{stream["tvg_name"]}" group-title="{stream["group_title"]}",{stream["name"]} ({stream["platform"]})'
        
        # Use web player for all streams
        stream_url = f"https://durgaa17.github.io/bblive9/player.html?stream={stream['id']}"
        
        m3u_content.append(extinf_line)
        m3u_content.append(stream_url)
    
    return "\n".join(m3u_content)

if __name__ == "__main__":
    print("🎯 Bigg Boss Tamil S9 - Version 3.0")
    print("🔄 Fetching best streams from multiple sources...")
    
    streams = get_best_streams()
    
    # Create output data
    output = {
        "version": "3.0",
        "last_updated": datetime.now(timezone.utc).isoformat(),
        "sources": streams,
        "total_sources": len(streams),
        "status": "success"
    }
    
    # Write JSON data
    with open('streams.json', 'w') as f:
        json.dump(output, f, indent=2)
    
    # Generate M3U playlists
    m3u_direct = generate_m3u_playlist(streams)
    m3u_web = generate_web_m3u_playlist(streams)
    
    # Write M3U files
    with open('playlist.m3u', 'w') as f:
        f.write(m3u_direct)
    
    with open('playlist_web.m3u', 'w') as f:
        f.write(m3u_web)
    
    print(f"✅ Version 3.0 Complete!")
    print(f"📊 Found {len(streams)} streams")
    print("📁 Files generated:")
    print("   - streams.json")
    print("   - playlist.m3u")
    print("   - playlist_web.m3u")
    
    # Show stream summary
    print("\n📺 Available Streams:")
    for stream in streams:
        print(f"   • {stream['name']} ({stream['platform']})")
