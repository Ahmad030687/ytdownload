from flask import Flask, request, send_file
import requests
import io
import json

app = Flask(__name__)

# 🦅 AHMAD RDX PRIVATE CONFIG
HF_TOKEN = "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"
# Naya Model URL (Stable Inference Path)
MODEL_URL = "https://router.huggingface.co/models/SG161222/RealVisXL_V4.0"

@app.route('/')
def home():
    return "🦅 Ahmad RDX Python API is Online!"

@app.route('/api/rdx-edit', methods=['GET'])
def rdx_edit():
    prompt = request.args.get('prompt')
    image_url = request.args.get('imageUrl')

    if not prompt or not image_url:
        return {"error": "Prompt aur ImageUrl lazmi hain ustad!"}, 400

    # 🎭 Heavy Generative Prompt
    final_prompt = f"Professional 3D name art. The name '{prompt}' written in massive glowing 3D golden letters. Background inspired by: {image_url}. Cinematic lighting, 8k, realistic."

    headers = {
        "Authorization": f"Bearer {HF_TOKEN}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(MODEL_URL, headers=headers, json={"inputs": final_prompt}, timeout=120)
        
        # 1. Check if model is loading (503)
        if response.status_code == 503:
            return {"error": "AI Engine is waking up. Please retry in 30 seconds."}, 503
        
        # 2. Check if request was successful
        if response.status_code == 200:
            return send_file(io.BytesIO(response.content), mimetype='image/png')
        
        # 3. Handle Errors without crashing .json()
        try:
            err_details = response.json()
        except:
            err_details = response.text # Agar JSON nahi hai toh raw text le lo

        return {"error": "AI Model Error", "status": response.status_code, "details": err_details}, response.status_code

    except Exception as e:
        return {"error": str(e)}, 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
