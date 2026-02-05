import os
import json
import yt_dlp
import time
from flask import Flask, request, jsonify, send_file

app = Flask(__name__)

# Temporary storage configuration
CACHE_DIR = "cache"
if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)

# ---------------------------------------------------------
# 🍪 COOKIE ENGINE (Keeping your identity safe)
# ---------------------------------------------------------
USER_COOKIES_JSON = [
    {"domain": ".youtube.com", "expirationDate": 1803152394, "name": "LOGIN_INFO", "path": "/", "secure": True, "value": "AFmmF2swRQIhAMflPTE6MoT2TFkiwe6ZABRluSYnR6afHZ9dSWdR9INrAiAdviaxgrqzqgZ0VsyNGO0EMkp9nWab944A6YfvXImy9A:QUQ3MjNmdzZESXY4TlBZUWxjX29uU0E0cXFXY0M4S3RaWXJGMEwtNXVvVjJKakdaLTVORzlLWExQaTFJNmk3cUh3ZFRNV2VWQkdwNGU3UDdGN2g0LURiSFJhSFB5WmJ4dlpmUlFZRURaenVqN3pJWTFjYVlXcnJBUDZxNjRTM1Rhd01xTlBfazdYUzdiRHM1S1kzZXpWZkEtbEloeG43SnF3"},
    {"domain": ".youtube.com", "expirationDate": 1800691058, "name": "__Secure-1PSIDTS", "path": "/", "secure": True, "value": "sidts-CjQB7I_69D4ahACgH7GPqCOt9nvns1CBZCkppJ-v_nn5D8V8GHE7oLbjlSVZwuDcJcnvLMH5EAA"},
    {"domain": ".youtube.com", "expirationDate": 1803715058, "name": "SID", "path": "/", "secure": False, "value": "g.a0006AiwL2hukjGc1ZVRNKS5XWaBxI-Fj77QIGyj8Cy21eiI1o1wjWmRXyGckSNQiebYLf5EpgACgYKAVgSARMSFQHGX2MiO0_dneDdrFrNJSf8t1qtCRoVAUF8yKqXONKm2DFycalJCILVjmYu0076"},
    {"domain": ".youtube.com", "expirationDate": 1803715058, "name": "__Secure-1PSID", "path": "/", "secure": True, "value": "g.a0006AiwL2hukjGc1ZVRNKS5XWaBxI-Fj77QIGyj8Cy21eiI1o1w0shnpaJpgEyf0phdztRj3AACgYKARwSARMSFQHGX2MiQryCG9kvP0GRC7sq9MTM9RoVAUF8yKp6rtzdOATqvqqqTZ1Zhszw0076"}
]

def create_cookie_file():
    cookie_path = "cookies.txt"
    with open(cookie_path, "w") as f:
        f.write("# Netscape HTTP Cookie File\n")
        for c in USER_COOKIES_JSON:
            domain = c.get("domain", ".youtube.com")
            flag = "TRUE" if domain.startswith(".") else "FALSE"
            path = c.get("path", "/")
            secure = "TRUE" if c.get("secure") else "FALSE"
            expiry = int(c.get("expirationDate", 0))
            name = c.get("name")
            value = c.get("value")
            f.write(f"{domain}\t{flag}\t{path}\t{secure}\t{expiry}\t{name}\t{value}\n")
    return cookie_path

COOKIE_FILE = create_cookie_file()

# ---------------------------------------------------------
# 🎥 CORE ROUTES
# ---------------------------------------------------------

@app.route('/')
def home():
    return "🦅 Ahmad RDX Private Engine is ONLINE."

@app.route('/yt-search')
def yt_search():
    query = request.args.get('q')
    if not query: return jsonify({"status": False})
    try:
        # Search doesn't need cookies usually, keeping it fast
        ydl_opts = {'quiet': True, 'extract_flat': True, 'default_search': 'ytsearch5'}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(query, download=False)
            results = [{"title": e['title'], "url": f"https://www.youtube.com/watch?v={e['id']}"} for e in info.get('entries', [])]
            return jsonify({"status": True, "results": results})
    except Exception as e:
        return jsonify({"status": False, "error": str(e)})

@app.route('/yt-download')
def yt_download():
    url = request.args.get('url')
    media_type = request.args.get('type', 'audio')
    if not url: return jsonify({"status": False, "msg": "URL missing"})

    try:
        # Naming the file
        file_id = f"res_{int(time.time())}"
        ext = "mp3" if media_type == "audio" else "mp4"
        file_path = os.path.join(CACHE_DIR, f"{file_id}.{ext}")

        # AHMAD RDX: THE UNIVERSAL FORMAT FIX
        # We use 'best' to ensure it picks a single stream that doesn't need FFmpeg
        ydl_opts = {
            'format': 'bestaudio/best' if media_type == 'audio' else 'best[ext=mp4]/best',
            'outtmpl': file_path,
            'cookiefile': COOKIE_FILE,
            'quiet': True,
            'nocheckcertificate': True,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        return send_file(file_path, as_attachment=True)
    except Exception as e:
        return jsonify({"status": False, "error": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
    
