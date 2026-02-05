from flask import Flask, request, jsonify
from googlesearch import search
import yt_dlp
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "🦅 Ahmad RDX - AI Search & Music/Video Engine Live!"

# --- 🔍 GOOGLE SEARCH ENGINE ---
@app.route('/api/google', methods=['GET'])
def google_search():
    query = request.args.get('q')
    if not query:
        return jsonify({"status": False, "error": "Query missing!"})
    try:
        results = []
        for j in search(query, num_results=5, advanced=True):
            results.append({"title": j.title, "link": j.url, "description": j.description})
        return jsonify({"status": True, "results": results})
    except Exception as e:
        return jsonify({"status": False, "error": str(e)})

# --- 🎵 MASTER SEARCH & DOWNLOAD ENGINE ---
def yt_search_and_extract(query, is_audio=True):
    # ytsearch:1 ka matlab hai pehla result uthao
    search_query = f"ytsearch1:{query}"
    
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'format': 'bestaudio/best' if is_audio else 'best[ext=mp4]/best',
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(search_query, download=False)
        if 'entries' in info:
            video = info['entries'][0]
        else:
            video = info
            
        return {
            "title": video.get('title'),
            "download_url": video.get('url'),
            "duration": video.get('duration'),
            "thumbnail": video.get('thumbnail'),
            "status": True
        }

@app.route('/api/search-music', methods=['GET'])
def search_music():
    q = request.args.get('q')
    if not q: return jsonify({"status": False, "error": "Song name missing!"})
    try:
        res = yt_search_and_extract(q, is_audio=True)
        return jsonify(res)
    except Exception as e:
        return jsonify({"status": False, "error": str(e)})

@app.route('/api/search-video', methods=['GET'])
def search_video():
    q = request.args.get('q')
    if not q: return jsonify({"status": False, "error": "Video name missing!"})
    try:
        res = yt_search_and_extract(q, is_audio=False)
        return jsonify(res)
    except Exception as e:
        return jsonify({"status": False, "error": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
    
