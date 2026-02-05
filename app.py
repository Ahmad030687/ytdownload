import os
import requests
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

# 🦅 AHMAD RDX - REAL NANO-BANANA BRIDGE
@app.route('/api/ai/geminiOption', methods=['GET'])
def gemini_nano_banana():
    prompt = request.args.get('prompt')
    image_url = request.args.get('imageUrl')
    cookie = request.args.get('cookie')
    
    if not prompt or not image_url or not cookie:
        return jsonify({"success": False, "error": "Missing parameters"}), 400

    try:
        # 1. Setup Session (Browser ki tarah dikhna zaroori hai)
        session = requests.Session()
        headers = {
            "Cookie": cookie,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            "Content-Type": "application/json",
            "Referer": "https://gemini.google.com/"
        }

        # 2. Gemini Chat Endpoint (NanoBanana works here)
        # Hum Google ke internal "Chat" endpoint ko hit karenge jo image processing karta hai
        api_url = "https://gemini.google.com/_/BardChatUi/data/assistant.lamda.BardChatUi/GetBardResponse"
        
        # Ye payload NanoBanana ka asali raaz hai
        payload = f'f.req=[null,"[[\\"{prompt}\\"],[\\"en\\"],null,[[\\"{image_url}\\\",1],null,\\"\\"]]"]&at=1'

        response = session.post(api_url, headers=headers, data=payload, timeout=60)
        
        # 3. Response Parsing
        # Gemini ka response boht complex hota hai, hum us mein se image link dhoondenge
        res_text = response.text
        
        # Yahan hum check karenge ke kya Gemini ne koi image generate ki hai
        if "http" in res_text:
            # Simple logic: Pehla milne wala googleusercontent link uthao
            import re
            links = re.findall(r'(https?://googleusercontent\.com/[^\s"\]]+)', res_text)
            
            if links:
                final_link = links[0]
            else:
                # Agar direct link nahi mila toh fallback (Simulation of success)
                return jsonify({"success": False, "error": "Gemini processed but no image link found in response"}), 500
        else:
            return jsonify({"success": False, "error": "Gemini rejected the request. Maybe cookies expired?"}), 500

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
        return jsonify({"success": False, "error": f"System Error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
    
