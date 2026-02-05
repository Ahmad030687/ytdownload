from flask import Flask, request, jsonify, send_file
import requests
import io
import random

app = Flask(__name__)

# 🦅 RDX MASTER GENERATOR ENGINE
def rdx_generator(prompt, style_prompt, image_url=None):
    seed = random.randint(1, 9999999)
    # Adding Nano-Banana Style Prompt Engineering
    final_prompt = f"{style_prompt}. User Prompt: {prompt}. "
    if image_url:
        final_prompt += f"Inspired by environment: {image_url}. "
    
    final_prompt += "8k resolution, cinematic lighting, highly detailed, professional art."
    
    # Using Flux for high-quality text and image blending
    url = f"https://image.pollinations.ai/prompt/{final_prompt}?width=1024&height=1024&nologo=true&model=flux&seed={seed}"
    return url

@app.route('/')
def health():
    return jsonify({"status": "Online", "owner": "AHMAD RDX", "commands_count": 22})

# --- 🎭 20+ COMMANDS ENDPOINTS ---

@app.route('/api/<style>', methods=['POST'])
def handle_api(style):
    data = request.json
    prompt = data.get('prompt', 'Beautiful Art')
    img_url = data.get('images', [None])[0] # Array format support

    # Styles Dictionary
    styles = {
        "create-v9": "Professional 3D golden name art, luxury aesthetic",
        "neon": "Vibrant 3D neon glass lettering, cyberpunk city background",
        "fire": "Realistic fire and flame textured 3D text, burning embers",
        "water": "Crystal clear water splash 3D typography, refreshing vibe",
        "cyberpunk": "High-tech cyberpunk style with futuristic blue and pink lighting",
        "anime": "Professional Studio Ghibli style anime illustration",
        "sketch": "Hand-drawn detailed pencil sketch art",
        "horror": "Dark, misty, scary horror movie poster style",
        "royal": "King style silver and diamond encrusted 3D name art",
        "nature": "Text made of green leaves and flowers, jungle aesthetic",
        "space": "Galactic nebula style, stars and planets background",
        "glitch": "Modern digital glitch and vaporwave aesthetic",
        "pixel": "Retro 8-bit pixel art style",
        "cartoon": "3D Disney Pixar style character and text",
        "gold-leaf": "Elegant gold leaf texture on black marble",
        "retro": "1980s synthwave retro style glowing grid",
        "glass": "Transparent frosted glass effect with soft shadows",
        "oil-paint": "Classical heavy brush stroke oil painting",
        "graffiti": "Street art graffiti style on urban brick wall",
        "magical": "Fantasy world with sparkles, fairies, and glowing dust",
        "minimalist": "Clean, simple, professional flat vector design",
        "metallic": "Shiny brushed metal chrome 3D effect"
    }

    if style not in styles:
        return jsonify({"error": "Style not found ustad!"}), 404

    target_url = rdx_generator(prompt, styles[style], img_url)
    
    try:
        response = requests.get(target_url, timeout=60)
        return send_file(io.BytesIO(response.content), mimetype='image/png')
    except:
        return jsonify({"error": "AI Server Busy"}), 502

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
    
