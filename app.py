from flask import Flask, request, jsonify
from googlesearch import search
import yt_dlp
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "🦅 Ahmad RDX - Private Search & Downloader API Live!"

# --- 🔍 GOOGLE SEARCH ENGINE ---
@app.route('/api/google', methods=['GET'])
def google_search():
    query = request.args.get('q')
    if not query:
        return jsonify({"error": "Query missing!"}), 400
    
    try:
        results = []
        # Top 5 results nikalne ke liye
        for j in search(query, num_results=5, advanced=True):
            results.append({
                "title": j.title,
                "link": j.url,
                "description": j.description
            })
        return jsonify({"status": True, "results": results})
    except Exception as e:
        return jsonify({"status": False, "error": str(e)}), 500

# --- 📥 YOUTUBE DOWNLOADER ENGINE ---
@app.route('/api/ytdl', methods=['GET'])
def youtube_download():
    video_url = request.args.get('url')
    if not video_url:
        return jsonify({"error": "URL missing!"}), 400

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
            
            return jsonify({
                "status": True,
                "title": title,
                "download_url": download_link
            })
    except Exception as e:
        return jsonify({"status": False, "error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
    
