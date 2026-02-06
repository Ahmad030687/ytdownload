from flask import Flask, request, jsonify, send_file
import yt_dlp
import requests
from bs4 import BeautifulSoup
import os
import io
import re
from PIL import Image, ImageOps

app = Flask(__name__)

# --- 🛠️ SETUP ---
FRAME_FILENAME = "premium_frame.png"
FRAME_URL = "https://i.postimg.cc/YSKjVG2w/1770355527236.png"
DEFAULT_AVATAR_URL = "https://i.imgur.com/5ki1g8T.png" 

if not os.path.exists(FRAME_FILENAME):
    try:
        r = requests.get(FRAME_URL)
        with open(FRAME_FILENAME, 'wb') as f: f.write(r.content)
    except: pass

@app.route('/')
def home():
    return "🦅 AHMAD RDX - Smart Bing Answer API Active!"

# ==========================================
# 🧠 ENGINE 1: BING TO-THE-POINT SEARCH
# ==========================================
@app.route('/api/search', methods=['GET'])
def search_engine():
    query = request.args.get('q')
    if not query: return jsonify({"status": False, "error": "Missing query"})
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        resp = requests.get(f"https://www.bing.com/search?q={query.replace(' ', '+')}", headers=headers, timeout=5)
        soup = BeautifulSoup(resp.text, 'html.parser')
        
        # 🎯 Targeted Search Logic
        # Sabse pehle Bing ka "Focus Answer" dhoondo, warna first result
        ans_box = soup.select_one('.b_focusTextMedium') or soup.select_one('.b_focusText') or soup.select_one('.b_caption p')
        
        if ans_box:
            raw_answer = ans_box.get_text().strip()
            
            # --- 🧹 CLEANING LOGIC (To-The-Point) ---
            # 1. Date headers hatana (e.g. "4 days ago · ")
            if " · " in raw_answer:
                raw_answer = raw_answer.split(" · ")[-1]
            
            # 2. Sirf pehla Sentence uthana (Stop at first dot)
            if "." in raw_answer:
                # Agar pehla dot boht jaldi hai (like Dr. ya Mr.), toh second dot tak dekho
                sentence = raw_answer.split(".")[0]
                if len(sentence) < 15 and "." in raw_answer[len(sentence)+1:]:
                     sentence = raw_answer.split(".")[0] + "." + raw_answer.split(".")[1]
                answer = sentence + "."
            else:
                answer = raw_answer

            return jsonify({
                "status": True, 
                "answer": answer,
                "brand": "🦅 AHMAD RDX"
            })
            
    except: pass

    return jsonify({"status": False, "error": "Jawab nahi mila ustad!"})

# ==========================================
# 📥 ENGINE 2: YOUTUBE (NO FFMPEG)
# ==========================================
@app.route('/api/ytdl', methods=['GET'])
def downloader():
    video_url = request.args.get('url')
    if not video_url: return jsonify({"status": False, "error": "URL missing"}), 400
    cookie_file = 'cookies.txt'
    if not os.path.exists(cookie_file): return jsonify({"status": False, "error": "cookies.txt missing"}), 500

    ydl_opts = {
        'format': 'best[ext=mp4]/best',
        'quiet': True, 'no_warnings': True, 'nocheckcertificate': True,
        'cookiefile': cookie_file, 'noplaylist': True, 'geo_bypass': True,
        'extractor_args': {'youtube': {'player_client': ['android', 'web']}}
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            download_url = info.get('url')
            if not download_url:
                for f in reversed(info.get('formats', [])):
                    if f.get('url') and f.get('protocol') in ['https', 'http']:
                        download_url = f['url']; break
            return jsonify({
                "status": True, "title": info.get('title'),
                "download_url": download_url, "author": "Ahmad RDX"
            })
    except Exception as e: return jsonify({"status": False, "error": str(e)}), 500

# ==========================================
# 🖼️ ENGINE 3: FRIEND FRAME
# ==========================================
@app.route('/api/friend', methods=['GET'])
def friend_frame():
    try:
        url1, url2 = request.args.get('url1'), request.args.get('url2')
        base = Image.open(FRAME_FILENAME).convert("RGBA")
        final_image = Image.new("RGBA", base.size)
        def process_img(url):
            try:
                resp = requests.get(url, stream=True, timeout=5)
                img = Image.open(io.BytesIO(resp.content)).convert("RGBA")
            except:
                img = Image.open(io.BytesIO(requests.get(DEFAULT_AVATAR_URL).content)).convert("RGBA")
            return ImageOps.fit(img, (320, 430), centering=(0.5, 0.5))
        final_image.paste(process_img(url1), (138, 165))
        final_image.paste(process_img(url2), (565, 165))
        final_image.paste(base, (0, 0), base)
        img_io = io.BytesIO()
        final_image.save(img_io, 'PNG')
        img_io.seek(0)
        return send_file(img_io, mimetype='image/png')
    except Exception as e: return {"error": str(e)}, 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
    
