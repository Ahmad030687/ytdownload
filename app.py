from flask import Flask, request, jsonify
import yt_dlp
import requests
from bs4 import BeautifulSoup
import random
import os

app = Flask(__name__)

# Rotate User-Agents for Bing
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
]

@app.route('/')
def home():
    return "🦅 𝐀𝐇𝐌𝐀𝐃 𝐑𝐃𝐗 - 𝐁𝐢𝐧𝐠 𝐒𝐞𝐚𝐫𝐜𝐡 & 𝐘𝐓 𝐃𝐨𝐰𝐧𝐥ｏ𝐚𝐝𝐞𝐫 𝐀ctive!"

# --- 🔍 BING SEARCH ENGINE (Real-Time Information) ---
@app.route('/api/ask', methods=['GET'])
def bing_search():
    query = request.args.get('q')
    if not query: return jsonify({"status": False, "error": "Ustad, sawal toh likho!"})

    headers = {"User-Agent": random.choice(USER_AGENTS)}
    results = []

    try:
        # Bing Search URL
        url = f"https://www.bing.com/search?q={query.replace(' ', '+')}"
        resp = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(resp.text, 'html.parser')

        # Bing results parsing logic
        for item in soup.select('li.b_algo')[:6]: # Top 6 results
            title = item.select_one('h2').get_text() if item.select_one('h2') else "No Title"
            link = item.select_one('a')['href'] if item.select_one('a') else ""
            snippet = item.select_one('.b_caption p, .b_linebtm')
            description = snippet.get_text() if snippet else "No description available."

            if link:
                results.append({
                    "title": title,
                    "link": link,
                    "description": description
                })

        if not results:
            return jsonify({"status": False, "msg": "Bing busy hai ya result nahi mila!"})

        return jsonify({
            "status": True,
            "query": query,
            "results": results,
            "brand": "𝐀𝐇𝐌𝐀𝐃 𝐑𝐃𝐗 𝐀𝐈"
        })

    except Exception as e:
        return jsonify({"status": False, "error": str(e)})

# --- 📥 YOUTUBE DOWNLOADER (Cookie & Fallback Enabled) ---
@app.route('/api/ytdl', methods=['GET'])
def youtube_download():
    video_url = request.args.get('url')
    req_type = request.args.get('type', 'video')
    
    if not video_url: return jsonify({"status": False, "error": "URL missing!"})

    # Sabse safe format logic
    format_logic = 'bestaudio/best' if req_type == 'audio' else '18/bestvideo+bestaudio/best'

    ydl_opts = {
        'format': format_logic,
        'quiet': True,
        'cookiefile': 'cookies.txt', # Netscape format file
        'user_agent': random.choice(USER_AGENTS),
        'nocheckcertificate': True
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
    
