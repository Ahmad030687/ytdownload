from flask import Flask, request, jsonify
import requests
import base64
from io import BytesIO
from PIL import Image
import random

app = Flask(__name__)

@app.route("/")
def home():
    return "🦅 AHMAD RDX – NANO BANANA PRO CLONE LIVE"

@app.route("/create-v9", methods=["POST"])
def generate():
    data = request.json
    prompt = data.get("prompt")
    # Nano Banana style: images array se pehli image uthana
    images = data.get("images", [])

    if not prompt:
        return jsonify({"status": False, "error": "Prompt missing hai ustad!"}), 400

    # 🦅 NANO PROMPT WRAPPER
    # Hum prompt ko "Heavy" banayenge taake result generic na lage
    heavy_prompt = (
        f"Professional 3D name art. Text: '{prompt}'. "
        f"Style: Glowing gold and neon glass, cinematic lighting, 8k, realistic masterpiece. "
    )
    
    # Agar user ne image di hai, toh hum usay description mein add karenge (Img2Img vibe)
    if images:
        heavy_prompt += f"Background and lighting inspired by: {images[0]}"

    seed = random.randint(1, 1000000)
    # Pollinations ka "Flux" model use kar rahe hain jo text rendering mein King hai
    img_url = f"https://image.pollinations.ai/prompt/{heavy_prompt}?width=1024&height=1024&nologo=true&model=flux&seed={seed}"

    try:
        r = requests.get(img_url, timeout=60)
        
        # Image ko base64 mein convert karna
        img = Image.open(BytesIO(r.content))
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        encoded = base64.b64encode(buffer.getvalue()).decode()

        return jsonify({
            "status": True,
            "brand": "𝐀𝐇𝐌𝐀𝐃 𝐑𝐃𝐗",
            "prompt": prompt,
            "image_base64": encoded
        })

    except Exception as e:
        return jsonify({"status": False, "error": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
    
