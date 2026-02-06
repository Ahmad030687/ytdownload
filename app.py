from flask import Flask, request, jsonify
import requests
import re

app = Flask(__name__)

@app.route('/')
def home():
    return "🦅 AHMAD RDX - Perfect Search API Active!"

# ==========================================
# 🧠 TO-THE-POINT SEARCH ENGINE
# ==========================================
@app.route('/api/search', methods=['GET'])
def search_engine():
    query = request.args.get('q')
    if not query:
        return jsonify({"status": False, "error": "Sawal missing hai!"})

    final_answer = ""

    try:
        # STEP 1: DuckDuckGo Instant Answer (Facts ke liye best)
        # Ye seedha "14 August 1947" ya "Islamabad" jaise jawab deta hai
        ddg_url = f"https://api.duckduckgo.com/?q={query}&format=json&no_html=1&skip_disambig=1"
        ddg_data = requests.get(ddg_url, timeout=5).json()

        if ddg_data.get("Answer"):
            final_answer = ddg_data.get("Answer")
        elif ddg_data.get("AbstractText"):
            final_answer = ddg_data.get("AbstractText")

        # STEP 2: Agar DDG se jawab nahi mila, toh Wikipedia Search
        if not final_answer:
            wiki_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{query.replace(' ', '_')}"
            wiki_resp = requests.get(wiki_url, timeout=5)
            if wiki_resp.status_code == 200:
                wiki_data = wiki_resp.json()
                final_answer = wiki_data.get("extract", "")

        # STEP 3: SAFFAI (Extra details hatana)
        if final_answer:
            # Sirf pehla sentence uthao (To-the-point)
            if "." in final_answer:
                final_answer = final_answer.split(".")[0] + "."
            
            # Junk words saaf karo
            final_answer = re.sub(r'\[\d+\]', '', final_answer) # Remove [1], [2]
            
            return jsonify({
                "status": True,
                "answer": final_answer,
                "brand": "🦅 AHMAD RDX"
            })
        else:
            return jsonify({"status": False, "error": "No direct answer found."})

    except Exception as e:
        return jsonify({"status": True, "answer": "Ustad, internet slow hai ya sawal mushkil hai. Dobara poochein!"})

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
    
