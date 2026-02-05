import os
import requests
import base64
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from io import BytesIO

app = Flask(__name__)
CORS(app)

# 🦅 AHMAD RDX - CUSTOM NANO BANANA BRIDGE
GEMINI_API_KEY = "AIzaSyBauxWLnLg9qujUA8xxBNeaDwr14q1Mdmo"
RAW_COOKIES = "SID=g.a0006QiwLyYuoTfkKUVNkbYYzc9QRSFaHVYRXTHOmZdf4LcBTeWmcvb4ugiOJ7qPFxXeozSZ9gACgYKATsSARMSFQHGX2Mivx6862AkewAphnDGuxFS5BoVAUF8yKo5px01bMIwGF7rMUnLrxWB0076; __Secure-1PSID=g.a0006QiwLyYuoTfkKUVNkbYYzc9QRSFaHVYRXTHOmZdf4LcBTeWmtYFGIZFcxBGElmMMkAnM2AACgYKAToSARMSFQHGX2MiMEr6sujisKxyvMSg3hZstRoVAUF8yKrVem0XeaBxpjsCOrrjzpaN0076; __Secure-3PSID=g.a0006QiwLyYuoTfkKUVNkbYYzc9QRSFaHVYRXTHOmZdf4LcBTeWmhe3hUUTPF-OQY9vD9HvMzAACgYKAbUSARMSFQHGX2MiPjP4zyW_5ejnoPUMHu6V5xoVAUF8yKpY9mayOt2nqN7kbaAhh46r0076;"

@app.route('/api/nano-banana', methods=['GET'])
def nano_banana():
    prompt = request.args.get('prompt')
    image_url = request.args.get('url')

    if not prompt or not image_url:
        return jsonify({"success": False, "error": "Parameters missing"}), 400

    try:
        # 1. IMAGE PROXY: Pehle photo ko download karke base64 banayenge
        response = requests.get(image_url)
        img_data = base64.b64encode(response.content).decode('utf-8')

        # 2. GEMINI AUTHENTICATION: Cookies ke saath request
        api_endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
        
        headers = {
            "Content-Type": "application/json",
            "Cookie": RAW_COOKIES
        }

        payload = {
            "contents": [{
                "parts": [
                    {"text": f"Instruction: {prompt}. Focus on high-quality editing. Output the edited image data."},
                    {"inline_data": {"mime_type": "image/jpeg", "data": img_data}}
                ]
            }]
        }

        # 3. CALLING GOOGLE ENGINE
        res = requests.post(api_endpoint, headers=headers, json=payload)
        res_json = res.json()

        # Result extracting logic (Anabot style)
        # Note: Agar Gemini image return karega to ham use URL mein badal denge
        try:
            # Agar Gemini link deta hai
            output_text = res_json['candidates'][0]['content']['parts'][0]['text'].strip()
            final_url = output_text if "http" in output_text else f"https://ytdownload-8wpk.onrender.com/api/proxy?prompt={prompt}&img={image_url}"
        except:
             # Fallback proxy link
             final_url = f"https://ytdownload-8wpk.onrender.com/api/proxy?prompt={prompt}&img={image_url}"

        return jsonify({
            "success": True,
            "status": 200,
            "author": "AHMAD RDX",
            "result": {
                "title": "NanoBanana Ultimate Edit",
                "prompt": prompt,
                "url": final_url
            }
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
    
