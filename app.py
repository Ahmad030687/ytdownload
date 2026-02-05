from flask import Flask, request, jsonify
import yt_dlp
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "🦅 Ahmad RDX - Music & Video Engine is 100% Active!"

# 🎵 Helper Function for Searching
def yt_search_and_extract(query, is_audio=True):
    # 'ytsearch1:' tells yt-dlp to pick the first result
    search_query = f"ytsearch1:{query}"
    
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'format': 'bestaudio/best' if is_audio else 'best[ext=mp4]/best',
        'noplaylist': True,
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(search_query, download=False)
        if 'entries' in info and len(info['entries']) > 0:
            video = info['entries'][0]
        else:
            video = info
            
        return {
            "status": True,
            "title": video.get('title'),
            "download_url": video.get('url'),
            "duration": video.get('duration'),
            "thumbnail": video.get('thumbnail'),
            "views": video.get('view_count'),
            "channel": video.get('uploader')
        }

# 🎧 Endpoint for #music
@app.route('/api/search-music', methods=['GET'])
def search_music():
    q = request.args.get('q')
    if not q: return jsonify({"status": False, "error": "Gaane ka naam do ustad!"})
    try:
        return jsonify(yt_search_and_extract(q, is_audio=True))
    except Exception as e:
        return jsonify({"status": False, "error": str(e)})

# 🎬 Endpoint for #video
@app.route('/api/search-video', methods=['GET'])
def search_video():
    q = request.args.get('q')
    if not q: return jsonify({"status": False, "error": "Video ka naam do ustad!"})
    try:
        return jsonify(yt_search_and_extract(q, is_audio=False))
    except Exception as e:
        return jsonify({"status": False, "error": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
    
