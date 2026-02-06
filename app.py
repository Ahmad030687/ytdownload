from flask import Flask, request, jsonify
import yt_dlp
import random

app = Flask(__name__)

@app.route('/api/ytdl', methods=['GET'])
def youtube_download():
    video_url = request.args.get('url')
    req_type = request.args.get('type', 'video')
    
    if not video_url:
        return jsonify({"status": False, "error": "URL missing!"}), 400

    # Format Logic: Sabse asaan aur working formats
    if req_type == 'audio':
        # Pehle best audio dhoondo, warna kuch bhi audio uthao
        format_str = 'bestaudio/best'
    else:
        # Pehle 360p ya 720p mp4, warna jo bhi best video ho
        format_str = 'best[ext=mp4]/best'

    ydl_opts = {
        'format': format_str,
        'quiet': True,
        'no_warnings': True,
        'nocheckcertificate': True,
        'cookiefile': 'cookies.txt',
        # Ye niche wali lines main hain jo error khatam karengi
        'extractor_args': {
            'youtube': {
                'player_client': ['android', 'web', 'mweb'],
                'skip': ['dash', 'hls']
            }
        },
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
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
        # Last Resort: Agar phir bhi error aaye toh har qism ka filter hata do
        try:
            ydl_opts['format'] = 'best'
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=False)
                return jsonify({
                    "status": True, 
                    "title": info.get('title'), 
                    "download_url": info.get('url'),
                    "msg": "Fallback mode used"
                })
        except:
            return jsonify({"status": False, "error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
    
