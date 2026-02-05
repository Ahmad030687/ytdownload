from flask import Flask, request, jsonify
import requests
import base64
import io
from PIL import Image
import torch
from diffusers import StableDiffusionInpaintPipeline

app = Flask(__name__)

# 🔥 Load Model (ONE TIME)
pipe = StableDiffusionInpaintPipeline.from_pretrained(
    "runwayml/stable-diffusion-inpainting",
    torch_dtype=torch.float32
)
pipe = pipe.to("cpu")  # Render free = CPU only

@app.route("/")
def home():
    return "🦅 AHMAD RDX IMAGE EDIT API - LIVE"

@app.route("/edit-image", methods=["POST"])
def edit_image():
    data = request.json

    image_url = data.get("image_url")
    prompt = data.get("prompt")

    if not image_url or not prompt:
        return jsonify({"status": False, "error": "image_url & prompt required"})

    try:
        # 📥 Download image
        img_data = requests.get(image_url).content
        image = Image.open(io.BytesIO(img_data)).convert("RGB")

        # ⚪ Auto mask (simple full edit)
        mask = Image.new("L", image.size, 255)

        # 🎨 Generate edited image
        result = pipe(
            prompt=prompt,
            image=image,
            mask_image=mask,
            num_inference_steps=25
        ).images[0]

        # 🔁 Convert to Base64
        buffered = io.BytesIO()
        result.save(buffered, format="PNG")
        img_base64 = base64.b64encode(buffered.getvalue()).decode()

        return jsonify({
            "status": True,
            "brand": "𝐀𝐇𝐌𝐀𝐃 𝐑𝐃𝐗",
            "prompt": prompt,
            "image_base64": img_base64
        })

    except Exception as e:
        return jsonify({"status": False, "error": str(e)})

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
