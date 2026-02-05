import os
from flask import Flask, request, jsonify, send_file
import yt_dlp

app = Flask(__name__)

# Temporary folder for files
CACHE_DIR = "cache"
if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)

@app.route('/')
def home():
    return "🦅 Ahmad RDX Private Download Engine is ACTIVE."

# ---------------------------------------------------------
# 📥 THE REAL DOWNLOADER (Ahmad RDX Custom Build)
# ---------------------------------------------------------
@app.route('/yt-download')
def yt_download():
    url = request.args.get('url')
    media_type = request.args.get('type', 'audio') # audio or video
    
    if not url: return jsonify({"status": False, "msg": "URL missing"})

    try:
        # File naming
        file_id = f"file_{os.urandom(4).hex()}"
        ext = "mp3" if media_type == "audio" else "mp4"
        file_path = os.path.join(CACHE_DIR, f"{file_id}.{ext}")

        # Ahmad Bhai: Ye settings YouTube ko 'ullu' banane ke liye hain
        ydl_opts = {
            'format': 'bestaudio/best' if media_type == 'audio' else 'best[ext=mp4]',
            'outtmpl': file_path,
            'quiet': True,
            'no_warnings': True,
            'nocheckcertificate': True,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        }

        # Actual downloading to Render server first
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        # Sending the file directly to your bot
        return send_file(file_path, as_attachment=True)

    except Exception as e:
        return jsonify({"status": False, "error": str(e)})

# Search route (Jo pehle se sahi chal raha hai)
@app.route('/yt-search')
def yt_search():
    query = request.args.get('q')
    if not query: return jsonify({"status": False})
    try:
        with yt_dlp.YoutubeDL({'quiet': True, 'extract_flat': True, 'default_search': 'ytsearch5'}) as ydl:
            info = ydl.extract_info(query, download=False)
            results = [{"title": e['title'], "url": f"https://www.youtube.com/watch?v={e['id']}"} for e in info['entries']]
            return jsonify({"status": True, "results": results})
    except:
        return jsonify({"status": False})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
