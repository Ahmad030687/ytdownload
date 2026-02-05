from flask import Flask, request, jsonify
import yt_dlp
import requests
from bs4 import BeautifulSoup
import random
import os

app = Flask(__name__)

# User agents rotate karne se block hone ka chance kam ho jata hai
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1"
]

@app.route('/')
def home():
    return "🦅 𝐀𝐇𝐌𝐀𝐃 𝐑𝐃𝐗 - 𝐒𝐦𝐚𝐫𝐭 𝐒𝐞𝐚𝐫𝐜𝐡 & 𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝𝐞𝐫 𝐢𝐬 𝐋𝐢𝐯𝐞!"

# --- 🔍 SMART SEARCH ENGINE (Fix for Google Busy/[] Results) ---
@app.route('/api/google', methods=['GET'])
def smart_search():
    query = request.args.get('q')
    if not query: return jsonify({"status": False, "error": "Query missing!"})

    results = []
    headers = {"User-Agent": random.choice(USER_AGENTS)}

    # 1. Pehle Google Try karein
    try:
        google_url = f"https://www.google.com/search?q={query}&hl=en"
        resp = requests.get(google_url, headers=headers, timeout=8)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, 'html.parser')
            for g in soup.select('div.g'):
                title = g.select_one('h3')
                link = g.select_one('a')
                if title and link:
                    results.append({"title": title.get_text(), "link": link['href']})
    except:
        pass

    # 2. Agar Google Busy hai toh DuckDuckGo (Backup) use karein
    if not results:
        try:
            ddg_url = f"https://duckduckgo.com/html/?q={query}"
            resp = requests.get(ddg_url, headers=headers, timeout=8)
            soup = BeautifulSoup(resp.text, 'html.parser')
            for r in soup.select('.result__body'):
                title = r.select_one('.result__title')
                link = r.select_one('.result__a')
                if title and link:
                    results.append({"title": title.get_text().strip(), "link": link['href']})
        except Exception as e:
            return jsonify({"status": False, "error": str(e)})

    return jsonify({"status": True, "results": results[:10]})

# --- 📥 YOUTUBE DOWNLOADER (Cookie Bypass Logic) ---
@app.route('/api/ytdl', methods=['GET'])
def youtube_download():
    video_url = request.args.get('url')
    req_type = request.args.get('type', 'video')
    
    if not video_url: return jsonify({"status": False, "error": "URL missing!"})

    ydl_opts = {
        'format': 'bestaudio/best' if req_type == 'audio' else 'best[ext=mp4]/best',
        'quiet': True,
        'no_warnings': True,
        'cookiefile': 'cookies.txt',  # Yeh file honi chahiye
        'nocheckcertificate': True,
        'user_agent': random.choice(USER_AGENTS),
        'extractor_args': {'youtube': {'player_client': ['android', 'web']}},
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            return jsonify({
                "status": True,
                "title": info.get('title'),
                "download_url": info.get('url'),
                "brand": "𝐀𝐇𝐌𝐀𝐃 𝐑𝐃𝐗"
            })
    except Exception as e:
        return jsonify({"status": False, "error": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
    
