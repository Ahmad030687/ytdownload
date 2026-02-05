from flask import Flask, request, jsonify
import yt_dlp
import requests
from bs4 import BeautifulSoup
import random
import time

app = Flask(__name__)

# 🎭 List of User-Agents taake block na ho
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
]

@app.route('/')
def home():
    return "🦅 Ahmad RDX - Anti-Bot Search & Downloader Live!"

# --- 🔍 GOOGLE SEARCH (NEW PRO METHOD) ---
@app.route('/api/google', methods=['GET'])
def google_search():
    query = request.args.get('q')
    if not query: return jsonify({"status": False, "error": "Query missing!"})

    headers = {"User-Agent": random.choice(USER_AGENTS)}
    try:
        # Direct scraping with headers to avoid 'Busy' error
        search_url = f"https://www.google.com/search?q={query}&num=10"
        response = requests.get(search_url, headers=headers, timeout=10)
        
        if response.status_code != 200:
            return jsonify({"status": False, "msg": "Google still blocking Render IP. Try again in 1 min."})

        soup = BeautifulSoup(response.text, 'html.parser')
        results = []
        
        # Google search results parsing logic
        for g in soup.find_all('div', class_='tF2Cxc'):
            title = g.find('h3').text if g.find('h3') else "No Title"
            link = g.find('a')['href'] if g.find('a') else ""
            desc = g.find('div', class_='VwiC3b').text if g.find('div', class_='VwiC3b') else ""
            if link:
                results.append({"title": title, "link": link, "description": desc})

        return jsonify({"status": True, "results": results})
    except Exception as e:
        return jsonify({"status": False, "error": str(e)})

# --- 📥 YOUTUBE DOWNLOADER (ANTI-BOT) ---
@app.route('/api/ytdl', methods=['GET'])
def youtube_download():
    video_url = request.args.get('url')
    req_type = request.args.get('type', 'video')

    if not video_url: return jsonify({"status": False, "error": "URL missing!"})

    # 🛡️ Anti-Bot Options
    ydl_opts = {
        'format': 'bestaudio/best' if req_type == 'audio' else 'best[ext=mp4]/best',
        'quiet': True,
        'no_warnings': True,
        'user_agent': random.choice(USER_AGENTS),
        'nocheckcertificate': True,
        'geo_bypass': True,
        # Agar block ho raha ho toh ye line zaroori hai
        'extractor_args': {'youtube': {'player_client': ['android', 'web']}}, 
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Extract info without downloading
            info = ydl.extract_info(video_url, download=False)
            return jsonify({
                "status": True,
                "title": info.get('title'),
                "download_url": info.get('url'),
                "thumbnail": info.get('thumbnail'),
                "brand": "𝐀𝐇𝐌𝐀𝐃 𝐑𝐃𝐗"
            })
    except Exception as e:
        # Agar "Sign in" error aaye toh ye message show hoga
        error_msg = str(e)
        if "Sign in to confirm you are not a bot" in error_msg:
            return jsonify({"status": False, "error": "YouTube blocked this request. Try again shortly."})
        return jsonify({"status": False, "error": error_msg})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
    
