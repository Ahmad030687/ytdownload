from flask import Flask, request, jsonify
import yt_dlp
import requests
from bs4 import BeautifulSoup
import random
import os

app = Flask(__name__)

# 🎭 Rotate User-Agents taake Google aur YouTube ko lage ke aslee log hain
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1"
]

@app.route('/')
def home():
    return "🦅 𝐀𝐇𝐌𝐀𝐃 𝐑𝐃𝐗 - 𝐌𝐮𝐥𝐭𝐢-𝐄𝐧𝐠𝐢𝐧𝐞 𝐀𝐏𝐈 𝐢𝐬 𝐋𝐢𝐯𝐞!"

# --- 🔍 GOOGLE SEARCH ENGINE (Fixed Scraper) ---
@app.route('/api/google', methods=['GET'])
def google_search():
    query = request.args.get('q')
    if not query:
        return jsonify({"status": False, "error": "Query missing ustad!"}), 400
    
    headers = {"User-Agent": random.choice(USER_AGENTS)}
    try:
        # Google search with headers and parameters to bypass bot detection
        url = f"https://www.google.com/search?q={query}&hl=en&num=10"
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code != 200:
            return jsonify({"status": False, "msg": "Google busy hai, please thori der baad try karein!"})

        soup = BeautifulSoup(response.text, 'html.parser')
        results = []

        # Professional parsing logic
        for g in soup.find_all('div', class_='tF2Cxc'):
            title = g.find('h3').text if g.find('h3') else "No Title"
            link = g.find('a')['href'] if g.find('a') else ""
            desc = g.find('div', class_='VwiC3b').text if g.find('div', class_='VwiC3b') else ""
            if link:
                results.append({"title": title, "link": link, "description": desc})

        if not results:
            return jsonify({"status": False, "msg": "Results khali hain, Render IP block ho rahi hai!"})

        return jsonify({"status": True, "results": results})
    except Exception as e:
        return jsonify({"status": False, "error": str(e)}), 500

# --- 📥 YOUTUBE DOWNLOADER (Cookie Supported) ---
@app.route('/api/ytdl', methods=['GET'])
def youtube_download():
    video_url = request.args.get('url')
    req_type = request.args.get('type', 'video') # audio or video
    
    if not video_url:
        return jsonify({"status": False, "error": "URL missing!"}), 400

    # yt-dlp Options with Cookie File
    ydl_opts = {
        'format': 'bestaudio/best' if req_type == 'audio' else 'best[ext=mp4]/best',
        'quiet': True,
        'no_warnings': True,
        'cookiefile': 'cookies.txt',  # Yeh file aapne project folder mein rakhni hai
        'nocheckcertificate': True,
        'user_agent': random.choice(USER_AGENTS),
        'geo_bypass': True,
        'extractor_args': {'youtube': {'player_client': ['android', 'web']}},
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            return jsonify({
                "status": True,
                "title": info.get('title'),
                "download_url": info.get('url'),
                "thumbnail": info.get('thumbnail'),
                "duration": f"{info.get('duration') // 60}:{info.get('duration') % 60:02d}",
                "brand": "𝐀𝐇𝐌𝐀𝐃 𝐑𝐃𝐗"
            })
    except Exception as e:
        error_msg = str(e)
        if "Sign in" in error_msg:
            return jsonify({"status": False, "error": "Cookies expire ho gayi hain ustad ji!"})
        return jsonify({"status": False, "error": error_msg}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
    
