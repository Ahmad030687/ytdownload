from flask import Flask, request, jsonify
import yt_dlp
import random

app = Flask(__name__)

@app.route('/api/ytdl', methods=['GET'])
def youtube_download():
    video_url = request.args.get('url')
    req_type = request.args.get('type', 'audio')
    
    if not video_url:
        return jsonify({"status": False, "error": "URL missing!"}), 400

    # Format Logic: Sabse simple 'ba' (best audio) ya 'b' (best)
    # Is se format available wala error hamesha ke liye khatam ho jata hai
    ydl_opts = {
        'format': 'ba/b' if req_type == 'audio' else 'bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]/b',
        'quiet': True,
        'no_warnings': True,
        'nocheckcertificate': True,
        'cookiefile': 'cookies.txt',
        'noplaylist': True,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-us,en;q=0.5',
        }
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # extract_info with download=False results in just the URL
            info = ydl.extract_info(video_url, download=False)
            
            # Agar format error phir bhi aaye, toh 'url' field check karein
            download_url = info.get('url')
            if not download_url:
                # Agar main url na mile toh formats list se uthao
                formats = info.get('formats', [])
                download_url = formats[-1].get('url') if formats else None

            return jsonify({
                "status": True,
                "title": info.get('title'),
                "download_url": download_url,
                "brand": "𝐀𝐇𝐌𝐀𝐃 𝐑𝐃𝐗"
            })
    except Exception as e:
        # Akhri koshish: Bilkul basic format
        try:
            with yt_dlp.YoutubeDL({'format': 'best', 'cookiefile': 'cookies.txt', 'quiet': True}) as ydl_fallback:
                info_fb = ydl_fallback.extract_info(video_url, download=False)
                return jsonify({
                    "status": True,
                    "title": info_fb.get('title'),
                    "download_url": info_fb.get('url'),
                    "msg": "Fallback success"
                })
        except Exception as last_error:
            return jsonify({"status": False, "error": str(last_error)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
    
