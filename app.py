import os
from flask import Flask, request, send_file
import requests
import io

app = Flask(__name__)

# 🦅 AHMAD RDX PRIVATE CONFIG (Now using Environment Variables)
# Ab ye token code mein nazar nahi aayega, isliye block nahi hoga!
HF_TOKEN = os.getenv("HF_TOKEN") 
MODEL_URL = "https://router.huggingface.co/models/SG161222/RealVisXL_V4.0"

@app.route('/')
def home():
    return "🦅 Ahmad RDX Python API (Security Fixed) is Online!"

@app.route('/api/rdx-edit', methods=['GET'])
def rdx_edit():
    # Security Check: Agar token nahi mila
    if not HF_TOKEN:
        return {"error": "HF_TOKEN is missing in Environment Variables!"}, 500

    prompt = request.args.get('prompt')
    image_url = request.args.get('imageUrl')

    if not prompt or not image_url:
        return {"error": "Prompt aur ImageUrl lazmi hain!"}, 400

    # 🎭 Premium Generative Prompt
    final_prompt = f"Professional 3D name art. The name '{prompt}' written in massive glowing 3D golden letters. Background vibe: {image_url}. Cinematic lighting, 8k resolution, realistic textures."

    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    
    try:
        response = requests.post(MODEL_URL, headers=headers, json={"inputs": final_prompt}, timeout=120)
        
        if response.status_code == 200:
            return send_file(io.BytesIO(response.content), mimetype='image/png')
        
        # Handle model loading or errors
        return {"error": "AI Model Error", "status": response.status_code, "msg": response.text}, response.status_code

    except Exception as e:
        return {"error": str(e)}, 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
