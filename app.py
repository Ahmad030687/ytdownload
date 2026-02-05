import os
import requests
import base64
from flask import Flask, request, jsonify

app = Flask(__name__)

# 🦅 AHMAD RDX PRIVATE NANO-BANANA ENGINE
GEMINI_KEY = "AIzaSyBauxWLnLg9qujUA8xxBNeaDwr14q1Mdmo"

@app.route('/api/ai/geminiOption', methods=['GET'])
def gemini_nano_banana():
    prompt = request.args.get('prompt')
    image_url = request.args.get('imageUrl')
    cookie = request.args.get('cookie')
    
    if not prompt or not image_url or not cookie:
        return jsonify({"success": False, "error": "Missing parameters (prompt, imageUrl, or cookie)"}), 400

    try:
        # 1. Image ko Fetch karna (Gemini ko bhejney ke liye)
        img_res = requests.get(image_url)
        img_base64 = base64.b64encode(img_res.content).decode('utf-8')

        # 2. Gemini Official API call with Cookies
        # Nano Banana ka kaam Vision Model se image manipulation karwana hai
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_KEY}"
        
        headers = {
            "Content-Type": "application/json",
            "Cookie": cookie
        }

        payload = {
            "contents": [{
                "parts": [
                    {"text": f"Instruction: {prompt}. Return only the direct URL of the edited image generated."},
                    {"inline_data": {"mime_type": "image/jpeg", "data": img_base64}}
                ]
            }]
        }

        response = requests.post(url, headers=headers, json=payload)
        res_json = response.json()

        # 3. Gemini Response se link nikalna
        try:
            # Gemini jo text deta hai us mein image link hota hai
            final_link = res_json['candidates'][0]['content']['parts'][0]['text'].strip()
            
            # Agar Gemini link nahi balkay text de raha hai, toh hum image processing trigger karenge
            if "http" not in final_link:
                # Fallback logic for NanoBanana simulation
                final_link = f"https://image.pollinations.ai/prompt/{prompt}?image={image_url}" # Sirf safety ke liye
        except:
            return jsonify({"success": False, "error": "Gemini failed to process image"}), 500

        # EXACT ANABOT FORMAT
        return jsonify({
            "success": True,
            "data": {
                "result": {
                    "url": final_link
                }
            },
            "author": "AHMAD RDX"
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
    
