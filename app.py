import os
import json
import yt_dlp
import time
from flask import Flask, request, jsonify, send_file

app = Flask(__name__)

# Temporary directory for media files
CACHE_DIR = "cache"
if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)

# ---------------------------------------------------------
# 🍪 COOKIE ENGINE: Aapki JSON cookies ko Netscape format mein badalna
# ---------------------------------------------------------
USER_COOKIES_JSON = [
    {"domain": ".youtube.com", "expirationDate": 1803152394, "name": "LOGIN_INFO", "path": "/", "secure": True, "value": "AFmmF2swRQIhAMflPTE6MoT2TFkiwe6ZABRluSYnR6afHZ9dSWdR9INrAiAdviaxgrqzqgZ0VsyNGO0EMkp9nWab944A6YfvXImy9A:QUQ3MjNmdzZESXY4TlBZUWxjX29uU0E0cXFXY0M4S3RaWXJGMEwtNXVvVjJKakdaLTVORzlLWExQaTFJNmk3cUh3ZFRNV2VWQkdwNGU3UDdGN2g0LURiSFJhSFB5WmJ4dlpmUlFZRURaenVqN3pJWTFjYVlXcnJBUDZxNjRTM1Rhd01xTlBfazdYUzdiRHM1S1kzZXpWZkEtbEloeG43SnF3"},
    {"domain": ".youtube.com", "expirationDate": 1800691058, "name": "__Secure-1PSIDTS", "path": "/", "secure": True, "value": "sidts-CjQB7I_69D4ahACgH7GPqCOt9nvns1CBZCkppJ-v_nn5D8V8GHE7oLbjlSVZwuDcJcnvLMH5EAA"},
    {"domain": ".youtube.com", "expirationDate": 1800691058, "name": "__Secure-3PSIDTS", "path": "/", "secure": True, "value": "sidts-CjQB7I_69D4ahACgH7GPqCOt9nvns1CBZCkppJ-v_nn5D8V8GHE7oLbjlSVZwuDcJcnvLMH5EAA"},
    {"domain": ".youtube.com", "expirationDate": 1803715058, "name": "HSID", "path": "/", "secure": False, "value": "A6KaP_-ZtpNx1DPWl"},
    {"domain": ".youtube.com", "expirationDate": 1803715058, "name": "SSID", "path": "/", "secure": True, "value": "A66EiYbsCbht8MeYB"},
    {"domain": ".youtube.com", "expirationDate": 1803715058, "name": "APISID", "path": "/", "secure": False, "value": "kJoi38dXpi617zgJ/A-mo03AzyHQVdg-IJ"},
    {"domain": ".youtube.com", "expirationDate": 1803715058, "name": "SAPISID", "path": "/", "secure": True, "value": "LNDiahU7YjO3eITT/A4JCBFbME6zDwTZT7"},
    {"domain": ".youtube.com", "expirationDate": 1803715058, "name": "SID", "path": "/", "secure": False, "value": "g.a0006AiwL2hukjGc1ZVRNKS5XWaBxI-Fj77QIGyj8Cy21eiI1o1wjWmRXyGckSNQiebYLf5EpgACgYKAVgSARMSFQHGX2MiO0_dneDdrFrNJSf8t1qtCRoVAUF8yKqXONKm2DFycalJCILVjmYu0076"},
    {"domain": ".youtube.com", "expirationDate": 1803715058, "name": "__Secure-1PSID", "path": "/", "secure": True, "value": "g.a0006AiwL2hukjGc1ZVRNKS5XWaBxI-Fj77QIGyj8Cy21eiI1o1w0shnpaJpgEyf0phdztRj3AACgYKARwSARMSFQHGX2MiQryCG9kvP0GRC7sq9MTM9RoVAUF8yKp6rtzdOATqvqqqTZ1Zhszw0076"},
    {"domain": ".youtube.com", "expirationDate": 1803715058, "name": "__Secure-3PSID", "path": "/", "secure": True, "value": "g.a0006AiwL2hukjGc1ZVRNKS5XWaBxI-Fj77QIGyj8Cy21eiI1o1wNsLYDwfK5-gnM6xL8sbmlgACgYKAYUSARMSFQHGX2Mi1XZWyT5TQqRG3nau4oJXqhoVAUF8yKoT8qoKY8qqh_cGeHt3h7L80076"}
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
            # Correct 7-column tab separated Netscape format
            f.write(f"{domain}\t{flag}\t{path}\t{secure}\t{expiry}\t{name}\t{value}\n")
    return cookie_path

COOKIE_FILE = create_cookie_file()

# ---------------------------------------------------------
# 🎥 ROUTES
# ---------------------------------------------------------

@app.route('/')
def home():
    return "🦅 Ahmad RDX Private Stealth Engine is ACTIVE."

# 1. Search Engine (Already Optimized)
@app.route('/yt-search')
def yt_search():
    query = request.args.get('q')
    if not query: return jsonify({"status": False, "msg": "Query missing"})
    try:
        ydl_opts = {
            'quiet': True,
            'extract_flat': True,
            'default_search': 'ytsearch5',
            'nocheckcertificate': True
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(query, download=False)
            results = [{"title": e['title'], "url": f"https://www.youtube.com/watch?v={e['id']}"} for e in info.get('entries', [])]
            return jsonify({"status": True, "results": results})
    except Exception as e:
        return jsonify({"status": False, "error": str(e)})

# 2. Universal Downloader (Fixed Format & Cookies)
@app.route('/yt-download')
def yt_download():
    url = request.args.get('url')
    media_type = request.args.get('type', 'audio')
    if not url: return jsonify({"status": False, "msg": "URL missing"})

    try:
        # File path setting
        file_id = f"res_{int(time.time())}"
        ext = "mp3" if media_type == "audio" else "mp4"
        file_path = os.path.join(CACHE_DIR, f"{file_id}.{ext}")

        # Ahmad RDX Fix: 
        # Render par FFmpeg aksar missing hota hai, isliye hum 'best' single file format mangenge
        ydl_opts = {
            'format': 'bestaudio/best' if media_type == 'audio' else 'best[ext=mp4]/best',
            'outtmpl': file_path,
            'cookiefile': COOKIE_FILE,
            'quiet': True,
            'nocheckcertificate': True,
            # Stealth: Mobile request bypass detection
            'extractor_args': {'youtube': {'player_client': ['mweb', 'android']}},
            'user_agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1'
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        return send_file(file_path, as_attachment=True)

    except Exception as e:
        return jsonify({"status": False, "error": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
            
