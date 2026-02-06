from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import re

app = Flask(__name__)

@app.route('/')
def home():
    return "🦅 𝐀𝐇𝐌𝐀𝐃 𝐑𝐃𝐗 - Perfect Direct Search Active!"

@app.route('/api/search', methods=['GET'])
def search_engine():
    query = request.args.get('q')
    if not query:
        return jsonify({"status": False, "error": "Query missing!"})

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
    }

    try:
        # 1. TRY BING FOR DIRECT ANSWER (Dates/Facts)
        bing_url = f"https://www.bing.com/search?q={query.replace(' ', '+')}"
        resp = requests.get(bing_url, headers=headers, timeout=5)
        soup = BeautifulSoup(resp.text, 'html.parser')

        # Target specific elements that contain the direct answer
        answer = None
        
        # A. Check for Bing Answer Box (The bold text at top)
        ans_box = soup.select_one('.b_focusTextMedium') or soup.select_one('.b_focusText') or soup.select_one('.rwrl')
        
        if ans_box:
            answer = ans_box.get_text().strip()
        else:
            # B. Fallback to Wikipedia Summary if no direct box
            wiki_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{query.replace(' ', '_')}"
            wiki_data = requests.get(wiki_url, timeout=5).json()
            answer = wiki_data.get('extract')

        if answer:
            # CLEANING: Remove extra dates like "4 days ago" and limit to first sentence
            # Removes "Feb 6, 2026 · " or similar patterns
            answer = re.sub(r'^[A-Za-z]+ \d+, \d+ · ', '', answer) 
            answer = re.sub(r'\[\d+\]', '', answer) # Remove citations [1]
            
            # To-the-point: Sirf pehla sentence
            if "." in answer:
                answer = answer.split(".")[0] + "."

            return jsonify({
                "status": True,
                "answer": answer,
                "brand": "𝐀𝐇𝐌𝐀𝐃 𝐑𝐃𝐗"
            })
        
        return jsonify({"status": False, "error": "Direct answer not found."})

    except Exception as e:
        return jsonify({"status": False, "error": "Server busy, try again."})

if __name__ == "__main__":
    import os
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
    
