import os
from flask import Flask, request, jsonify
import requests
import base64
import io

app = Flask(__name__)

# 🦅 AHMAD RDX PRO CONFIG
# Segmind ya Replicate ki API Key (Ye bilkul private hoti hai)
# Is se aapka result 100% "Pure Nano-Banana" jaisa aayega
API_KEY = "SG_bc779b89667da8d3" # Yahan apni API Key dalein
MODEL_URL = "https://api.segmind.com/v1/sdxl1.0-img2img"

@app.route("/")
def home():
    return "🦅 AHMAD RDX – PURE PRIVATE AI ENGINE LIVE"

@app.route("/edit", methods=["POST"])
def edit():
    try:
        data = request.json
        prompt = data.get("prompt")
        image_url = data.get("imageUrl") # Nano-Banana URL leta hai

        if not prompt or not image_url:
            return jsonify({"status": False, "error": "Missing prompt or imageUrl"}), 400

        # 🎭 Professional SDXL Parameters
        payload = {
            "prompt": f"Professional 3D name art, {prompt}, glowing gold letters, cinematic lighting, 8k, realistic masterpiece",
            "negative_prompt": "blurry, low quality, distorted, ugly",
            "image": image_url,
            "strength": 0.75,
            "guidance_scale": 12,
            "samples": 1,
            "scheduler": "UniPC",
            "num_inference_steps": 30
        }

        headers = {'x-api-key': API_KEY}

        # 🚀 Calling the Pure AI Node
        response = requests.post(MODEL_URL, json=payload, headers=headers)

        if response.status_code == 200:
            # Direct Image stream back to bot
            img_base64 = base64.b64encode(response.content).decode()
            return jsonify({
                "status": True,
                "brand": "𝐀𝐇𝐌𝐀𝐃 𝐑𝐃𝐗",
                "image_base64": img_base64
            })
        else:
            return jsonify({"status": False, "error": response.text}), response.status_code

    except Exception as e:
        return jsonify({"status": False, "error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
    
