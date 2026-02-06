from flask import Flask, request, send_file, jsonify
from PIL import Image, ImageOps, ImageDraw, ImageFont
import io, requests, os

app = Flask(__name__)

FRAME_URL = "https://i.postimg.cc/YSKjVG2w/1770355527236.png"

@app.route("/")
def home():
    return "🦅 AHMAD RDX Dost API Working"

@app.route("/api/dost", methods=["POST"])
def dost():
    try:
        if "u1" not in request.files or "u2" not in request.files:
            return jsonify({"status": False, "error": "Images missing"}), 400

        img1 = Image.open(request.files["u1"]).convert("RGBA")
        img2 = Image.open(request.files["u2"]).convert("RGBA")

        name1 = request.form.get("name1", "")
        name2 = request.form.get("name2", "")

        frame = Image.open(io.BytesIO(requests.get(FRAME_URL).content)).convert("RGBA")
        canvas = Image.new("RGBA", frame.size)

        img1 = ImageOps.fit(img1, (320, 430), centering=(0.5, 0.5))
        img2 = ImageOps.fit(img2, (320, 430), centering=(0.5, 0.5))

        canvas.paste(img1, (138, 165))
        canvas.paste(img2, (565, 165))
        canvas.paste(frame, (0, 0), frame)

        draw = ImageDraw.Draw(canvas)
        try:
            font = ImageFont.truetype("DejaVuSans-Bold.ttf", 32)
        except:
            font = ImageFont.load_default()

        draw.text((200, 610), name1, fill="white", font=font)
        draw.text((630, 610), name2, fill="white", font=font)

        buf = io.BytesIO()
        canvas.save(buf, format="PNG")
        buf.seek(0)

        return send_file(buf, mimetype="image/png")

    except Exception as e:
        return jsonify({"status": False, "error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
