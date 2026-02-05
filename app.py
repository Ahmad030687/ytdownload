from flask import Flask, request, jsonify
from googlesearch import search
import yt_dlp
import os
import random
import time

app = Flask(__name__)

# 🦅 RDX MASTER CONFIG
@app.route('/')
def home():
    return "🦅 Ahmad RDX - Ultimate Downloader & Search Engine is LIVE!"

# --- 🔍 GOOGLE SEARCH (FIXED) ---
# Google aksar block karta hai, is liye hum ne 'sleep' aur 'advanced' parameters set kiye hain
@app.route('/api/google', methods=['GET'])
def google_search():
    query = request.args.get('q')
    if not query:
        return jsonify({"status": False, "error": "Query missing ustad!"}), 400
    
    try:
        results = []
        # 'sleep_interval' dala hai taake Google block na kare
        # 'advanced=True' se description bhi mil jati hai
        for j in search(query, num_results=10, advanced=True, sleep_interval=2):
            results.append({
                "title": j.title,
                "link": j.url,
                "description": j.description
            })
            
        if not results:
            return jsonify({"status": False, "msg": "Google busy hai, thori der baad try karein!"})

        return jsonify({"status": True, "results": results})
    except Exception as e:
        return jsonify({"status": False, "error": str(e)}), 500

# --- 📥 YOUTUBE DOWNLOADER (AUDIO & VIDEO) ---
@app.route('/api/ytdl', methods=['GET'])
def youtube_download():
    video_url = request.args.get('url')
    # User batayega ke 'audio' chahiye ya 'video'
    req_type = request.args.get('type', 'video') 
    
    if not video_url:
        return jsonify({"status": False, "error": "URL missing!"}), 400

    # Format Logic: Audio ke liye sirf best audio, video ke liye best mp4
    if req_type == 'audio':
        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'no_warnings': True,
        }
    else:
        ydl_opts = {
            'format': 'best[ext=mp4]/best',
            'quiet': True,
            'no_warnings': True,
        }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            download_link = info.get('url')
            title = info.get('title')
            duration = info.get('duration')
            thumbnail = info.get('thumbnail')
            
            return jsonify({
                "status": True,
                "title": title,
                "format": req_type,
                "download_url": download_link,
                "duration": f"{duration // 60}:{duration % 60:02d}",
                "thumbnail": thumbnail,
                "brand": "𝐀𝐇𝐌𝐀𝐃 𝐑𝐃𝐗"
            })
    except Exception as e:
        return jsonify({"status": False, "error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
    
