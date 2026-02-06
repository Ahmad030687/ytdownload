from flask import Flask, request, jsonify, send_file
import requests
from bs4 import BeautifulSoup
import random
import os
import io
from PIL import Image, ImageOps

app = Flask(__name__)

# --- 🛠️ SETUP: AUTO-DOWNLOAD FRAME ---
# Ye function check karega ke frame server par hai ya nahi.
# Agar nahi hoga, toh aapke diye gaye link se download kar lega.
FRAME_FILENAME = "premium_frame.png"
FRAME_URL = "https://i.postimg.cc/YSKjVG2w/1770355527236.png"

def check_and_download_frame():
    if not os.path.exists(FRAME_FILENAME):
        print("📥 Downloading Premium Frame...")
        try:
            response = requests.get(FRAME_URL)
            if response.status_code == 200:
                with open(FRAME_FILENAME, 'wb') as f:
                    f.write(response.content)
                print("✅ Frame Saved Successfully!")
            else:
                print("❌ Failed to download frame.")
        except Exception as e:
            print(f"❌ Error downloading frame: {e}")

# Server start hote hi frame check karo
check_and_download_frame()

# --- 🎭 PRO HEADERS (For Search Engine) ---
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
    return "🦅 𝐀𝐇𝐌𝐀𝐃 𝐑𝐃𝐗 - Premium API Active!"

# ==========================================
# 🔍 ENGINE 1: INTELLIGENT SEARCH (BING + DDG)
# ==========================================
@app.route('/api/search', methods=['GET'])
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
# 🖼️ ENGINE 2: PREMIUM FRIEND FRAME
# ==========================================
@app.route('/api/friend', methods=['GET'])
def friend_frame():
    try:
        # Check if frame exists, if not try downloading again
        if not os.path.exists(FRAME_FILENAME):
            check_and_download_frame()
            if not os.path.exists(FRAME_FILENAME):
                return {"error": "Frame image not found on server."}, 500

        url1 = request.args.get('url1')
        url2 = request.args.get('url2')

        if not url1 or not url2: return {"error": "URLs missing"}, 400

        # 1. Load Base Frame
        base = Image.open(FRAME_FILENAME).convert("RGBA")
        
        # 2. Create Canvas
        final_image = Image.new("RGBA", base.size)

        # 3. Image Processor Function
        def process_img(url, size):
            resp = requests.get(url, stream=True)
            resp.raise_for_status()
            img = Image.open(io.BytesIO(resp.content)).convert("RGBA")
            img = ImageOps.fit(img, size, centering=(0.5, 0.5))
            return img

        # 🛠️ FRAME COORDINATES SETTINGS
        # Frame ke hisab se exact settings (Gold/Silver Side-by-Side)
        FRAME_WIDTH = 320   # Photo ki choraai
        FRAME_HEIGHT = 430  # Photo ki lambai
        
        # Left Photo Position (X, Y)
        LEFT_POS = (138, 165)
        
        # Right Photo Position (X, Y)
        RIGHT_POS = (565, 165)

        # Process Images
        img1 = process_img(url1, (FRAME_WIDTH, FRAME_HEIGHT))
        img2 = process_img(url2, (FRAME_WIDTH, FRAME_HEIGHT))

        # 4. COMPOSITING (Jodna)
        # Pehle photos lagayenge (Peeche)
        final_image.paste(img1, LEFT_POS)
        final_image.paste(img2, RIGHT_POS)
        
        # Phir uske upar Frame lagayenge (Taake borders photo ke upar aayen)
        final_image.paste(base, (0, 0), base)

        # 5. Send Result
        img_io = io.BytesIO()
        final_image.save(img_io, 'PNG')
        img_io.seek(0)
        return send_file(img_io, mimetype='image/png')

    except Exception as e:
        return {"error": str(e)}, 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
    
