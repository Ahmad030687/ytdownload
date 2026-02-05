from flask import Flask, request, jsonify
import yt_dlp
import requests
from bs4 import BeautifulSoup
import random
import os

app = Flask(__name__)

# Rotate User-Agents to mimic different browsers
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
]

@app.route('/')
def home():
    return "🦅 𝐀𝐇𝐌𝐀𝐃 𝐑𝐃𝐗 - 𝐔𝐥𝐭𝐢𝐦𝐚ｔ𝐞 𝐀𝐏𝐈 𝐢𝐬 𝐋𝐢𝐯ｅ!"

# --- 🔍 SMART SEARCH (Google + DuckDuckGo Fallback) ---
@app.route('/api/google', methods=['GET'])
def smart_search():
    query = request.args.get('q')
    if not query: return jsonify({"status": False, "error": "Query missing!"})

    results = []
    headers = {"User-Agent": random.choice(USER_AGENTS)}

    # Try Google First
    try:
        url = f"https://www.google.com/search?q={query}&hl=en"
        resp = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(resp.text, 'html.parser')
        # Professional selectors that work more often
        for g in soup.select('div.tF2Cxc, div.g, div.kvH9eb'):
            title = g.select_one('h3')
            link = g.select_one('a')
            if title and link:
                results.append({"title": title.get_text(), "link": link['href']})
    except:
        pass

    # If Google fails (results empty), Use DuckDuckGo
    if not results:
        try:
            ddg_url = f"https://duckduckgo.com/html/?q={query}"
            resp = requests.get(ddg_url, headers=headers, timeout=10)
            soup = BeautifulSoup(resp.text, 'html.parser')
            for r in soup.select('.result__body'):
                title = r.select_one('.result__title')
                link = r.select_one('.result__a')
                if title and link:
                    results.append({"title": title.get_text().strip(), "link": link['href']})
        except:
            return jsonify({"status": False, "error": "Search engines are busy!"})

    return jsonify({"status": True, "results": results[:10]})

# --- 📥 YOUTUBE DOWNLOADER (Multi-Format Support) ---
@app.route('/api/ytdl', methods=['GET'])
def youtube_download():
    video_url = request.args.get('url')
    req_type = request.args.get('type', 'video') # audio or video
    
    if not video_url: return jsonify({"status": False, "error": "URL missing!"})

    # Fix: Multi-format selection string taake "Format not available" error na aaye
    if req_type == 'audio':
        format_str = 'bestaudio/best'
    else:
        # Pehle mp4 check karega, agar nahi toh best video uthayega
        format_str = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'

    ydl_opts = {
        'format': format_str,
        'quiet': True,
        'no_warnings': True,
        'cookiefile': 'cookies.txt', # Make sure cookies.txt is in Netscape format
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
        # Fallback to absolute 'best' if specific format fails
        try:
            ydl_opts['format'] = 'best'
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=False)
                return jsonify({
                    "status": True,
                    "title": info.get('title'),
                    "download_url": info.get('url'),
                    "brand": "𝐀𝐇𝐌𝐀𝐃 𝐑𝐃𝐗"
                })
        except:
            return jsonify({"status": False, "error": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
    
