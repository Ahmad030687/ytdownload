from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import random

app = Flask(__name__)

# 🎭 Real-time User Agents
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3 Mobile/15E148 Safari/604.1"
]

@app.route('/')
def home():
    return "🦅 Ahmad RDX - Real-Time Search Engine Live!"

# --- 🚀 REAL-TIME SEARCH ENGINE API ---
@app.route('/api/search', methods=['GET'])
def search_engine():
    query = request.args.get('q')
    if not query:
        return jsonify({"status": False, "error": "Search query missing!"})

    headers = {"User-Agent": random.choice(USER_AGENTS)}
    results = []

    try:
        # DuckDuckGo ka use kar rahe hain real-time info ke liye (No Blocks)
        search_url = f"https://duckduckgo.com/html/?q={encode_query(query)}"
        response = requests.get(search_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extracting results
            for r in soup.select('.result__body')[:7]: # Top 7 results
                title = r.select_one('.result__title').get_text().strip()
                link = r.select_one('.result__a')['href']
                snippet = r.select_one('.result__snippet').get_text().strip()
                
                results.append({
                    "title": title,
                    "link": link,
                    "description": snippet
                })

        if not results:
            return jsonify({"status": False, "msg": "Real-time data busy, try again!"})

        return jsonify({
            "status": True,
            "query": query,
            "results": results,
            "brand": "𝐀𝐇𝐌𝐀𝐃 𝐑𝐃𝐗 𝐒𝐄𝐀𝐑𝐂𝐇"
        })

    except Exception as e:
        return jsonify({"status": False, "error": str(e)})

def encode_query(query):
    return query.replace(" ", "+")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
    
