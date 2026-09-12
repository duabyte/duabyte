import json
import os
import urllib.parse
import urllib.request
import html

USERNAME = "DuaaByte"
API_KEY = os.environ["LAST_API"]

params = urllib.parse.urlencode({
    "method": "user.getrecenttracks",
    "user": USERNAME,
    "api_key": API_KEY,
    "format": "json",
    "limit": 1
})

url = f"https://ws.audioscrobbler.com/2.0/?{params}"

try:
    with urllib.request.urlopen(url, timeout=10) as response:
        data = json.loads(response.read().decode())
except Exception as e:
    print(f"Error fetching Last.fm data: {e}")
    data = {}

tracks = data.get("recenttracks", {}).get("track", [])

if tracks:
    track = tracks[0]

    name = html.escape(track.get("name", "Unknown Track"))
    artist = html.escape(track.get("artist", {}).get("#text", "Unknown Artist"))
    now_playing = track.get("@attr", {}).get("nowplaying") == "true"

    if now_playing:
        title = "NOW PLAYING"
        icon = "▶"
    else:
        title = "LAST PLAYED"
        icon = "♪"
else:
    name = "Nothing playing"
    artist = "Start playing something"
    title = "CURRENTLY PLAYING"
    icon = "♪"

svg = f'''<svg width="500" height="120"
viewBox="0 0 500 120"
xmlns="http://www.w3.org/2000/svg">

<rect width="500" height="120" rx="15" fill="#1e1a24"/>

<text x="25" y="35" font-family="Arial, sans-serif" font-size="14" font-weight="bold" fill="#C9B8E8">
  {icon} {title}
</text>

<text x="25" y="65" font-family="Arial, sans-serif" font-size="18" font-weight="bold" fill="white">
  {name}
</text>

<text x="25" y="92" font-family="Arial, sans-serif" font-size="14" fill="#aaa">
  {artist}
</text>

</svg>
'''

with open("currently-playing.svg", "w", encoding="utf-8") as file:
    file.write(svg)

print(f"Updated: {icon} {title} - {name} by {artist}")