from flask import Flask, request, jsonify
import yt_dlp
import requests
from bs4 import BeautifulSoup
import random
import json
import os

app = Flask(__name__)

# 🍪 AHMAD RDX COOKIES DATA
# Maine aapki cookies yahan paste kar di hain
COOKIES_JSON = [
    {"domain": ".youtube.com", "name": "LOGIN_INFO", "value": "AFmmF2swRQIhAMflPTE6MoT2TFkiwe6ZABRluSYnR6afHZ9dSWdR9INrAiAdviaxgrqzqgZ0VsyNGO0EMkp9nWab944A6YfvXImy9A:QUQ3MjNmdzZESXY4TlBZUWxjX29uU0E0cXFXY0M4S3RaWXJGMEwtNXVvVjJKakdaLTVORzlLWExQaTFJNmk3cUh3ZFRNV2VWQkdwNGU3UDdGN2g0LURiSFJhSFB5WmJ4dlpmUlFZRURaenVqN3pJWTFjYVlXcnJBUDZxNjRTM1Rhd01xTlBfazdYUzdiRHM1S1kzZXpWZkEtbEloeG43SnF3"},
    {"domain": ".youtube.com", "name": "PREF", "value": "f6=40000000&tz=Asia.Karachi"},
    {"domain": ".youtube.com", "name": "__Secure-1PSIDTS", "value": "sidts-CjQB7I_69FHLYWJgiO0QHtenC_gqduc8rkmT9MnDHS0BZlGCCY74xfN1IP53dGL7Y2Cyi98TEAA"},
    {"domain": ".youtube.com", "name": "__Secure-3PSIDTS", "value": "sidts-CjQB7I_69FHLYWJgiO0QHtenC_gqduc8rkmT9MnDHS0BZlGCCY74xfN1IP53dGL7Y2Cyi98TEAA"},
    {"domain": ".youtube.com", "name": "HSID", "value": "Ath3zBq8dh0CyBv5T"},
    {"domain": ".youtube.com", "name": "SSID", "value": "Aw7LJqwKGzuUqq0Pp"},
    {"domain": ".youtube.com", "name": "APISID", "value": "TXAuWqcLxVqM9gsy/AZfSZ1RADQjbS_qqc"},
    {"domain": ".youtube.com", "name": "SAPISID", "value": "jfGEetuq2LhNFL1O/AFLTbRz0sk_Vmtg7Z"},
    {"domain": ".youtube.com", "name": "SID", "value": "g.a0006QiwLyYuoTfkKUVNkbYYzc9QRSFaHVYRXTHOmZdf4LcBTeWmcvb4ugiOJ7qPFxXeozSZ9gACgYKATsSARMSFQHGX2Mivx6862AkewAphnDGuxFS5BoVAUF8yKo5px01bMIwGF7rMUnLrxWB0076"},
    {"domain": ".youtube.com", "name": "__Secure-1PSID", "value": "g.a0006QiwLyYuoTfkKUVNkbYYzc9QRSFaHVYRXTHOmZdf4LcBTeWmtYFGIZFcxBGElmMMkAnM2AACgYKAToSARMSFQHGX2MiMEr6sujisKxyvMSg3hZstRoVAUF8yKrVem0XeaBxpjsCOrrjzpaN0076"},
    {"domain": ".youtube.com", "name": "__Secure-3PSID", "value": "g.a0006QiwLyYuoTfkKUVNkbYYzc9QRSFaHVYRXTHOmZdf4LcBTeWmhe3hUUTPF-OQY9vD9HvMzAACgYKAbUSARMSFQHGX2MiPjP4zyW_5ejnoPUMHu6V5xoVAUF8yKpY9mayOt2nqN7kbaAhh46r0076"}
]

# Function to save cookies in a file (yt-dlp needs a file)
def save_cookies():
    with open('cookies.json', 'w') as f:
        json.dump(COOKIES_JSON, f)

save_cookies()

@app.route('/')
def home():
    return "🦅 Ahmad RDX - Anti-Bot Downloader Engine Active!"

# --- 🔍 GOOGLE SEARCH (BYPASS BUSY) ---
@app.route('/api/google', methods=['GET'])
def google_search():
    query = request.args.get('q')
    if not query: return jsonify({"status": False, "error": "Query missing!"})
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        # Direct URL to avoid 'Busy' message
        url = f"https://www.google.com/search?q={query}&hl=en"
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        results = []
        for g in soup.find_all('div', class_='tF2Cxc'):
            title = g.find('h3').text if g.find('h3') else ""
            link = g.find('a')['href'] if g.find('a') else ""
            if title and link:
                results.append({"title": title, "link": link})
        
        # Fallback: Agar results khali hon (Render IP block)
        if not results:
            return jsonify({"status": False, "msg": "Google busy hai, DuckDuckGo try karun ustad?"})

        return jsonify({"status": True, "results": results})
    except Exception as e:
        return jsonify({"status": False, "error": str(e)})

# --- 📥 YOUTUBE DOWNLOADER (COOKIE ENABLED) ---
@app.route('/api/ytdl', methods=['GET'])
def youtube_download():
    video_url = request.args.get('url')
    req_type = request.args.get('type', 'video')

    if not video_url: return jsonify({"status": False, "error": "URL missing!"})

    ydl_opts = {
        'format': 'bestaudio/best' if req_type == 'audio' else 'best[ext=mp4]/best',
        'quiet': True,
        'no_warnings': True,
        'cookiefile': 'cookies.json', # Asli Magic yahan hai!
        'nocheckcertificate': True,
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
        return jsonify({"status": False, "error": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
    
