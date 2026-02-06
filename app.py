from flask import Flask, request, send_file, jsonify
import requests, io, os
from PIL import Image, ImageOps, ImageDraw, ImageFont

app = Flask(__name__)

@app.route('/')
def home():
    return "🦅 AHMAD RDX - Dost Frame API Active!"

@app.route('/api/dost', methods=['GET'])
def dost_frame():
    try:
        FRAME_URL = "https://i.postimg.cc/YSKjVG2w/1770355527236.png"

        u1 = request.args.get("u1")
        u2 = request.args.get("u2")
        n1 = request.args.get("n1", "Friend 1")
        n2 = request.args.get("n2", "Friend 2")

        if not u1 or not u2:
            return jsonify({"status": False, "error": "Missing image URLs"}), 400

        frame = Image.open(io.BytesIO(requests.get(FRAME_URL).content)).convert("RGBA")
        canvas = Image.new("RGBA", frame.size)

        def avatar(url):
            img = Image.open(io.BytesIO(requests.get(url).content)).convert("RGBA")
            return ImageOps.fit(img, (320, 430), centering=(0.5, 0.5))

        a1 = avatar(u1)
        a2 = avatar(u2)

        canvas.paste(a1, (138, 165))
        canvas.paste(a2, (565, 165))
        canvas.paste(frame, (0, 0), frame)

        # ✍️ Names draw
        draw = ImageDraw.Draw(canvas)
        try:
            font = ImageFont.truetype("arial.ttf", 36)
        except:
            font = ImageFont.load_default()

        draw.text((210, 610), n1, fill="white", font=font)
        draw.text((640, 610), n2, fill="white", font=font)

        out = io.BytesIO()
        canvas.save(out, format="PNG")
        out.seek(0)

        return send_file(out, mimetype="image/png")

    except Exception as e:
        return jsonify({"status": False, "error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
