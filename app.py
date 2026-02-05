from flask import Flask, request, send_file
import requests
import io

app = Flask(__name__)

# 🦅 AHMAD RDX PRIVATE CONFIG (UPDATED ROUTER URL)
HF_TOKEN = "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"
# Purana URL: https://api-inference.huggingface.co/...
# Naya URL: https://router.huggingface.co/...
MODEL_URL = "https://router.huggingface.co/models/SG161222/RealVisXL_V4.0"

@app.route('/')
def home():
    return "🦅 Ahmad RDX Python API (Router Edition) is Running!"

@app.route('/api/rdx-edit', methods=['GET'])
def rdx_edit():
    prompt = request.args.get('prompt')
    image_url = request.args.get('imageUrl')

    if not prompt or not image_url:
        return {"error": "Prompt aur ImageUrl lazmi hain ustad!"}, 400

    # 🎭 Heavy Generative Prompt Engineering
    final_prompt = f"Professional 3D name art. The name '{prompt}' written in massive glowing 3D golden letters. Background and aesthetic inspired by: {image_url}. Cinematic lighting, 8k resolution, realistic textures."

    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    
    try:
        # Calling Hugging Face Router
        response = requests.post(MODEL_URL, headers=headers, json={"inputs": final_prompt}, timeout=120)
        
        # Check for model loading
        if response.status_code == 503:
            return {"error": "AI Engine is waking up. Retry in 30 seconds."}, 503
        
        if response.status_code != 200:
            return {"error": "AI Model Error", "details": response.json()}, response.status_code

        # Sending the image back
        return send_file(io.BytesIO(response.content), mimetype='image/png')

    except Exception as e:
        return {"error": str(e)}, 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
