from flask import Flask, request, jsonify, send_file
import requests
import io
import os
from PIL import Image, ImageOps

app = Flask(__name__)

@app.route('/')
def home():
    return "🦅 AHMAD RDX - Dost Frame API Active!"

@app.route('/api/dost', methods=['GET'])
def dost_frame():
    try:
        # Aapka Diya Hua Frame Link
        FRAME_URL = "https://i.postimg.cc/YSKjVG2w/1770355527236.png"
        
        # User 1 aur User 2 ki PFP links
        u1_url = request.args.get('u1')
        u2_url = request.args.get('u2')

        if not u1_url or not u2_url:
            return jsonify({"status": False, "error": "Missing image URLs"}), 400

        # 1. Frame Load Karein
        frame_resp = requests.get(FRAME_URL, stream=True, timeout=10)
        base_frame = Image.open(io.BytesIO(frame_resp.content)).convert("RGBA")
        
        # 2. Base Canvas Banayein
        canvas = Image.new("RGBA", base_frame.size)

        def process_avatar(url):
            # Photo download karein
            resp = requests.get(url, stream=True, timeout=10)
            img = Image.open(io.BytesIO(resp.content)).convert("RGBA")
            # 🛡️ AUTOMATIC FIT: (320, 430) size mein photo fit karna
            # Ye chehra center mein rakhega aur baki extra hissa kaat dega
            return ImageOps.fit(img, (320, 430), centering=(0.5, 0.5))

        # 3. Dono Photos Process Karein
        avatar1 = process_avatar(u1_url)
        avatar2 = process_avatar(u2_url)

        # 4. Paste Karein (Coordinates Fixed)
        canvas.paste(avatar1, (138, 165))
        canvas.paste(avatar2, (565, 165))
        
        # 5. Frame ko sabse upar rakhein
        canvas.paste(base_frame, (0, 0), base_frame)

        # 6. Final Image Send Karein
        img_io = io.BytesIO()
        canvas.save(img_io, 'PNG')
        img_io.seek(0)
        return send_file(img_io, mimetype='image/png')

    except Exception as e:
        return jsonify({"status": False, "error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
    
