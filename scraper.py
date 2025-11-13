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
        },
        {
            'name': 'TamilDhool',
            'url': 'https://tamildhool.art/vijay-tv/vijay-tv-show/bigg-boss-tamil-s9/bigg-boss-tamil-s9-live-stream-24x7-vijay-tv-show-2/',
            'priority': 2
        },
        {
            'name': 'TamilTVSerial',
            'url': 'https://www.tamiltvserial.com/bigg-boss-tamil-9-live-24x7-stream-bigg-boss-9-tamil-live/',
            'priority': 2
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
            streams.extend(source_streams)
            
        except Exception as e:
            print(f"  Error with {source['name']}: {e}")
    
    # Remove duplicates and prioritize
    unique_streams = remove_duplicate_streams(streams)
    
    # Add direct Twitch channels as backup
    twitch_channels = [
        {'channel': 'arivumani1075', 'name': 'Arivumani 1075'},
        {'channel': 'arivumani1076', 'name': 'Arivumani 1076'},
        {'channel': 'tamillive', 'name': 'Tamil Live'},
        {'channel': 'tamilstream', 'name': 'Tamil Stream'}
    ]
    
    for twitch in twitch_channels:
        unique_streams.append({
            'id': len(unique_streams) + 1,
            'name': f"Bigg Boss - {twitch['name']}",
            'url': f"https://www.twitch.tv/{twitch['channel']}",
            'embed_url': f"https://player.twitch.tv/?channel={twitch['channel']}&parent=durgaa17.github.io",
            'platform': 'Twitch',
            'channel': twitch['channel'],
            'direct_url': f"https://www.twitch.tv/{twitch['channel']}",
            'type': 'twitch_direct',
            'quality': 'live',
            'source': 'Twitch Direct'
        })
    
    return unique_streams[:8]  # Return top 8 streams max

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
            'id': len(streams) + 1,
            'name': f"Bigg Boss Stream {len(streams) + 1}",
            'url': src,
            'platform': platform,
            'channel': channel,
            'embed_url': src,
            'direct_url': get_direct_url(src, platform, channel),
            'type': 'embedded',
            'quality': 'adaptive',
            'source': source_name,
            'tvg_id': f"BiggBoss{len(streams) + 1}",
            'tvg_name': f"Bigg Boss {platform}",
            'group_title': "Bigg Boss Tamil S9"
        }
        
        # Customize name based on platform and channel
        if platform == 'Twitch' and channel:
            stream_data['name'] = f"Bigg Boss - {channel}"
            stream_data['tvg_name'] = f"Bigg Boss {channel}"
        
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
        # Use web player fallback for OK.ru
        return f"https://durgaa17.github.io/bblive9/player.html?source=okru"
    else:
        # For other platforms, use the original URL
        return url

def remove_duplicate_streams(streams):
    """Remove duplicate streams based on URL"""
    seen_urls = set()
    unique_streams = []
    
    for stream in streams:
        # Create a unique identifier for the stream
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
    print(f"📊 Found {len(streams)} unique streams")
    print("📁 Files generated:")
    print("   - streams.json")
    print("   - playlist.m3u (Direct URLs)")
    print("   - playlist_web.m3u (Web player)")
    print("\n🎯 M3U URLs for IPTV:")
    print("   https://durgaa17.github.io/bblive9/playlist.m3u")
    print("   https://durgaa17.github.io/bblive9/playlist_web.m3u")
    
    # Show stream summary
    print("\n📺 Available Streams:")
    for stream in streams:
        print(f"   • {stream['name']} ({stream['platform']}) - {stream['source']}")
