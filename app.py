from flask import Flask, request, jsonify
import yt_dlp
import random

app = Flask(__name__)

@app.route('/')
def home():
    return "🦅 Ahmad RDX - Final Downloader Active!"

@app.route('/api/ytdl', methods=['GET'])
def youtube_download():
    video_url = request.args.get('url')
    req_type = request.args.get('type', 'audio')
    
    if not video_url:
        return jsonify({"status": False, "error": "URL missing!"}), 400

    # Sabse "SAFE" format logic: 
    # 'ba' = best audio, 'b' = best available. 
    # Format selection ko simple rakha hai taake error na aaye.
    ydl_opts = {
        'format': 'ba/b' if req_type == 'audio' else 'best',
        'quiet': True,
        'no_warnings': True,
        'nocheckcertificate': True,
        'cookiefile': 'cookies.txt',
        'noplaylist': True,
        # Yeh line sabse zaroori hai error khatam karne ke liye:
        'extractor_args': {
            'youtube': {
                'player_client': ['android', 'ios'],
                'skip': ['hls', 'dash']
            }
        },
        'user_agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36'
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Extract info logic
            info = ydl.extract_info(video_url, download=False)
            
            # Direct link nikalne ki koshish
            download_url = info.get('url')
            
            # Agar direct link na mile toh formats mein dhoondo
            if not download_url:
                for f in info.get('formats', []):
                    if f.get('url'):
                        download_url = f['url']
                        break

            return jsonify({
                "status": True,
                "title": info.get('title'),
                "download_url": download_url,
                "brand": "𝐀𝐇𝐌𝐀𝐃 𝐑𝐃𝐗"
            })
            
    except Exception as e:
        # EK AKHRI KOSHISH: Agar sab fail ho jaye
        try:
            with yt_dlp.YoutubeDL({'format': 'best', 'cookiefile': 'cookies.txt'}) as ydl_retry:
                info_retry = ydl_retry.extract_info(video_url, download=False)
                return jsonify({
                    "status": True,
                    "title": info_retry.get('title'),
                    "download_url": info_retry.get('url'),
                    "msg": "Recovered with Best Format"
                })
        except:
            return jsonify({"status": False, "error": "YouTube is blocking this video on Render. Update cookies!"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
    
