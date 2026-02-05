from flask import Flask, request, jsonify
import yt_dlp
import requests
from bs4 import BeautifulSoup
import random
import os

app = Flask(__name__)

# Fake browser identity
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
]

@app.route('/')
def home():
    return "🦅 𝐀𝐇𝐌𝐀𝐃 𝐑𝐃𝐗 - 𝐁𝐮𝐥𝐥𝐞𝐭𝐩𝐫𝐨𝐨𝐟 𝐀𝐏𝐈 𝐢𝐬 𝐋𝐢𝐯𝐞!"

# --- 🔍 SMART SEARCH (DuckDuckGo Primary - No More [] Results) ---
@app.route('/api/google', methods=['GET'])
def smart_search():
    query = request.args.get('q')
    if not query: return jsonify({"status": False, "error": "Query missing!"})

    results = []
    headers = {"User-Agent": random.choice(USER_AGENTS)}

    # Google nakhre karta hai, is liye seedha DuckDuckGo par jao jo hamesha chalta hai
    try:
        ddg_url = f"https://duckduckgo.com/html/?q={query}"
        resp = requests.get(ddg_url, headers=headers, timeout=10)
        soup = BeautifulSoup(resp.text, 'html.parser')
        
        for r in soup.select('.result__body'):
            title = r.select_one('.result__title')
            link = r.select_one('.result__a')
            if title and link:
                results.append({
                    "title": title.get_text().strip(),
                    "link": link['href']
                })
        
        if not results:
            return jsonify({"status": False, "msg": "No results found even on backup engine!"})

        return jsonify({"status": True, "results": results[:10]})

    except Exception as e:
        return jsonify({"status": False, "error": str(e)})

# --- 📥 YOUTUBE DOWNLOADER (Auto-Format Fallback) ---
@app.route('/api/ytdl', methods=['GET'])
def youtube_download():
    video_url = request.args.get('url')
    req_type = request.args.get('type', 'video')
    
    if not video_url: return jsonify({"status": False, "error": "URL missing!"})

    # Sabse "SAFE" format jo har video ke liye available hota hai
    # itag 18 = 360p MP4 (Hamesha chalta hai)
    # best = Kuch bhi mil jaye
    format_logic = 'bestaudio/best' if req_type == 'audio' else '18/bestvideo+bestaudio/best'

    ydl_opts = {
        'format': format_logic,
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
        # AGAR PHIR BHI ERROR AAYE, TOH SABSE BASIC 'BEST' USE KARO
        try:
            ydl_opts['format'] = 'best'
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=False)
                return jsonify({
                    "status": True,
                    "title": info.get('title'),
                    "download_url": info.get('url'),
                    "brand": "𝐀𝐇𝐌𝐀𝐃 𝐑𝐃𝐗 (Fallback Mode)"
                })
        except:
            return jsonify({"status": False, "error": f"YouTube is blocking Render: {str(e)}"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
    
