from flask import Flask, request, jsonify
import yt_dlp
import random

app = Flask(__name__)

@app.route('/')
def home():
    return "🦅 Ahmad RDX - Pure Downloader Engine Active!"

@app.route('/api/ytdl', methods=['GET'])
def youtube_download():
    video_url = request.args.get('url')
    req_type = request.args.get('type', 'video') # audio ya video
    
    if not video_url:
        return jsonify({"status": False, "error": "URL missing!"}), 400

    # Format logic: Agar specific format na mile toh best uthao
    if req_type == 'audio':
        format_str = 'bestaudio/best'
    else:
        format_str = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'

    ydl_opts = {
        'format': format_str,
        'quiet': True,
        'no_warnings': True,
        'nocheckcertificate': True,
        'cookiefile': 'cookies.txt', # Cookies file lazmi upload karein
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
        return jsonify({"status": False, "error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
    
