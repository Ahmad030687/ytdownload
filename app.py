from flask import Flask, request, jsonify, send_file
import yt_dlp
import requests
from bs4 import BeautifulSoup
import random
import os
import io
from PIL import Image, ImageDraw, ImageFont, ImageOps

app = Flask(__name__)

# --- 🎭 PRO HEADERS (Anti-Block Logic) ---
def get_headers():
    return {
        "User-Agent": random.choice([
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36"
        ]),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Referer": "https://www.google.com/"
    }

@app.route('/')
def home():
    return "🦅 𝐀𝐇𝐌𝐀𝐃 𝐑𝐃𝐗 - All-in-One API Engine Live!"

# ==========================================
# 🔍 ENGINE 1: INTELLIGENT SEARCH (BING + DDG)
# ==========================================
@app.route('/api/ask', methods=['GET'])
def ask_engine():
    query = request.args.get('q')
    if not query: return jsonify({"status": False, "error": "Query missing!"})

    results = []
    
    # 1. Try Bing First
    try:
        resp = requests.get(f"https://www.bing.com/search?q={query.replace(' ', '+')}", headers=get_headers(), timeout=10)
        soup = BeautifulSoup(resp.text, 'html.parser')
        for item in soup.select('li.b_algo')[:5]:
            title = item.select_one('h2').get_text() if item.select_one('h2') else ""
            link = item.select_one('a')['href'] if item.select_one('a') else ""
            desc = item.select_one('.b_caption p').get_text() if item.select_one('.b_caption p') else ""
            if title and link:
                results.append({"title": title, "link": link, "description": desc})
    except: pass

    # 2. Fallback to DuckDuckGo if Bing fails
    if not results:
        try:
            resp = requests.get(f"https://duckduckgo.com/html/?q={query.replace(' ', '+')}", headers=get_headers(), timeout=10)
            soup = BeautifulSoup(resp.text, 'html.parser')
            for r in soup.select('.result__body')[:5]:
                results.append({
                    "title": r.select_one('.result__title').get_text().strip(),
                    "link": r.select_one('.result__a')['href'],
                    "description": r.select_one('.result__snippet').get_text().strip()
                })
        except: pass

    return jsonify({"status": True if results else False, "results": results, "brand": "𝐀𝐇𝐌𝐀𝐃 𝐑𝐃𝐗"})

# ==========================================
# 📥 ENGINE 2: MEDIA DOWNLOADER (YT + TIKTOK)
# ==========================================
@app.route('/api/ytdl', methods=['GET'])
def youtube_download():
    video_url = request.args.get('url')
    req_type = request.args.get('type', 'audio') # audio or video
    
    if not video_url: return jsonify({"status": False, "error": "URL missing!"}), 400

    # Smart Format Logic (To avoid 'Format Not Available' error)
    ydl_opts = {
        'format': 'ba/b' if req_type == 'audio' else 'best', # Safe Mode
        'quiet': True,
        'no_warnings': True,
        'nocheckcertificate': True,
        'cookiefile': 'cookies.txt', # Netscape cookies lazmi upload karein
        'noplaylist': True,
        'extractor_args': {
            'youtube': {
                'player_client': ['android', 'ios'], # Mobile client bypass
                'skip': ['hls', 'dash']
            }
        },
        'user_agent': get_headers()["User-Agent"]
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            dl_link = info.get('url') or (info['formats'][-1]['url'] if 'formats' in info else None)
            
            return jsonify({
                "status": True,
                "title": info.get('title'),
                "download_url": dl_link,
                "duration": info.get('duration_string'),
                "brand": "𝐀𝐇𝐌𝐀𝐃 𝐑𝐃𝐗"
            })
    except Exception as e:
        return jsonify({"status": False, "error": str(e)}), 500

# ==========================================
# 🖼️ ENGINE 3: AESTHETIC GRAPHICS (FRIEND FRAME)
# ==========================================
@app.route('/api/friend', methods=['GET'])
def friend_frame():
    try:
        url1 = request.args.get('url1')
        url2 = request.args.get('url2')
        name1 = request.args.get('name1', 'Friend')
        name2 = request.args.get('name2', 'Friend')

        if not url1 or not url2: return {"error": "URLs missing"}, 400

        # Canvas Setup
        W, H = 1000, 600
        background = Image.new('RGB', (W, H), color='#151515') # Premium Dark Black
        draw = ImageDraw.Draw(background)

        # Image Processor
        def process_img(url):
            resp = requests.get(url)
            img = Image.open(io.BytesIO(resp.content)).convert("RGB")
            return ImageOps.fit(img, (350, 350), centering=(0.5, 0.5))

        img1 = process_img(url1)
        img2 = process_img(url2)

        # --- DRAWING ---
        gold_color = "#FFD700"
        
        # Borders (Left & Right)
        draw.rectangle([45, 95, 405, 455], outline=gold_color, width=8) 
        background.paste(img1, (50, 100))
        
        draw.rectangle([595, 95, 955, 455], outline=gold_color, width=8)
        background.paste(img2, (600, 100))

        # Connector Line
        draw.line([405, 275, 595, 275], fill=gold_color, width=3)
        # Heart Center
        draw.ellipse([480, 255, 520, 295], fill="#E50914", outline=gold_color, width=2)

        # Fonts (Fallback Logic)
        try:
            # Linux server fonts
            font_bold = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 50)
            font_reg = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 28)
            font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
        except:
            font_bold = ImageFont.load_default()
            font_reg = ImageFont.load_default()
            font_small = ImageFont.load_default()

        # Text Overlay
        draw.text((W/2, 50), "BEST FRIENDS FOREVER", font=font_bold, fill=gold_color, anchor="mm")
        
        quote = "Side by side or miles apart,\nreal friends are always close to the heart."
        draw.multiline_text((W/2, 520), quote, font=font_reg, fill="white", anchor="mm", align="center")

        draw.text((225, 480), name1, font=font_small, fill="white", anchor="mm")
        draw.text((775, 480), name2, font=font_small, fill="white", anchor="mm")

        # Output
        img_io = io.BytesIO()
        background.save(img_io, 'PNG')
        img_io.seek(0)
        return send_file(img_io, mimetype='image/png')

    except Exception as e:
        return {"error": str(e)}, 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
    
