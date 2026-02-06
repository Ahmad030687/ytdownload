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
DEFAULT_AVATAR = "https://i.imgur.com/5ki1g8T.png"

if not os.path.exists(FRAME_FILENAME):
    try: requests.get(FRAME_URL).content and open(FRAME_FILENAME, 'wb').write(requests.get(FRAME_URL).content)
    except: pass

@app.route('/')
def home(): return "🦅 AHMAD RDX - Direct Answer API Active!"

# ==========================================
# 🧠 ENGINE 1: TO-THE-POINT ANSWER (No Bullshit)
# ==========================================
@app.route('/api/search', methods=['GET'])
def direct_answer():
    query = request.args.get('q')
    if not query: return jsonify({"status": False, "error": "Sawal missing hai!"})

    # Cleaning Logic: Faltu words hatane ke liye
    def clean_text(text):
        # 1. Citations hatana [1], [2]
        text = re.sub(r'\[\d+\]', '', text)
        # 2. Dates hatana (e.g. "4 days ago · ")
        if " · " in text:
            text = text.split(" · ")[-1]
        if "..." in text and len(text) < 20: # Agar shuru mein dots hain
            text = text.replace("...", "").strip()
        # 3. Sirf pehla jumla (First Sentence Only)
        # Ye sabse zaroori hai taake description na bane
        if "." in text:
            text = text.split(".")[0] + "."
        return text

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    final_answer = None

    try:
        # STRATEGY 1: DuckDuckGo Instant Answer API (Best for Facts/Math)
        # Ye seedha "4" ya "14 August" deta hai
        ddg_url = f"https://api.duckduckgo.com/?q={query}&format=json"
        ddg_resp = requests.get(ddg_url, timeout=3).json()
        
        if ddg_resp.get("Answer"):
            final_answer = ddg_resp.get("Answer")
        elif ddg_resp.get("AbstractText"):
            final_answer = ddg_resp.get("AbstractText")
        
        # STRATEGY 2: Google/Bing Snippet Scraping (Backup)
        if not final_answer:
            url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
            resp = requests.get(url, headers=headers, timeout=5)
            soup = BeautifulSoup(resp.text, 'html.parser')

            # Google "Featured Snippet" Class (B0prTE)
            snippet = soup.select_one('.B0prTE') or soup.select_one('.hgKElc') or soup.select_one('.kno-rdesc span')
            
            if snippet:
                final_answer = snippet.get_text().strip()
            else:
                # Agar snippet na mile to description ka pehla jumla
                desc = soup.select_one('.VwiC3b')
                if desc:
                    final_answer = desc.get_text().strip()

    except Exception as e:
        return jsonify({"status": False, "error": str(e)})

    if final_answer:
        # Aakhri safai (To The Point banane ke liye)
        final_answer = clean_text(final_answer)
        return jsonify({
            "status": True,
            "answer": final_answer,
            "brand": "🦅 AHMAD RDX"
        })
    else:
        return jsonify({"status": False, "error": "Answer nahi mila."})

# ==========================================
# 📥 ENGINE 2: YOUTUBE (No Fail Mode)
# ==========================================
@app.route('/api/ytdl', methods=['GET'])
def downloader():
    video_url = request.args.get('url')
    if not video_url: return jsonify({"status": False, "error": "URL missing"}), 400

    cookie_file = 'cookies.txt'
    if not os.path.exists(cookie_file): return jsonify({"status": False, "error": "cookies.txt missing"}), 500

    ydl_opts = {
        'format': 'best[ext=mp4]/best', # No FFmpeg needed
        'quiet': True, 'no_warnings': True, 'nocheckcertificate': True,
        'cookiefile': cookie_file, 'noplaylist': True, 'geo_bypass': True, 'ignoreerrors': True,
        'extractor_args': {'youtube': {'player_client': ['android', 'web']}}
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            if not info: return jsonify({"status": False, "error": "No info"}), 404
            
            download_url = info.get('url')
            if not download_url:
                for f in reversed(info.get('formats', [])):
                    if f.get('url') and f.get('protocol') in ['https', 'http']:
                        download_url = f['url']; break
            
            if not download_url: return jsonify({"status": False, "error": "Link nahi mila"}), 404

            return jsonify({
                "status": True,
                "title": info.get('title'),
                "download_url": download_url,
                "author": "Ahmad RDX"
            })
    except Exception as e: return jsonify({"status": False, "error": str(e)}), 500

# ==========================================
# 🖼️ ENGINE 3: FRIEND FRAME (Locked ID Fix)
# ==========================================
@app.route('/api/friend', methods=['GET'])
def friend_frame():
    try:
        url1 = request.args.get('url1')
        url2 = request.args.get('url2')
        if not url1 or not url2: return {"error": "URLs missing"}, 400

        if not os.path.exists(FRAME_FILENAME): requests.get(FRAME_URL)
        try: base = Image.open(FRAME_FILENAME).convert("RGBA")
        except: return {"error": "Base frame error"}, 500

        final_image = Image.new("RGBA", base.size)

        def process_img(url):
            try:
                resp = requests.get(url, stream=True, timeout=5)
                resp.raise_for_status()
                img = Image.open(io.BytesIO(resp.content)).convert("RGBA")
            except:
                img = Image.open(io.BytesIO(requests.get(DEFAULT_AVATAR).content)).convert("RGBA")
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
        
