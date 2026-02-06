from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

GEMINI_KEY = os.environ.get("GEMINI_API_KEY")

@app.route("/")
def home():
    return "🦅 AHMAD RDX GEMINI ASK API - LIVE"

@app.route("/api/search")
def search():
    q = request.args.get("q")
    if not q:
        return jsonify({"status": False, "error": "Query missing"})

    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_KEY}"

        payload = {
            "contents": [{
                "parts": [{
                    "text": f"Answer briefly and clearly:\nQ: {q}\nA:"
                }]
            }]
        }

        r = requests.post(url, json=payload, timeout=30)
        data = r.json()

        answer = data["candidates"][0]["content"]["parts"][0]["text"]
        answer = answer.split("\n")[0].strip()[:300]

        return jsonify({
            "status": True,
            "brand": "𝐀𝐇𝐌𝐀𝐃 𝐑𝐃𝐗",
            "question": q,
            "answer": answer
        })

    except Exception as e:
        return jsonify({"status": False, "error": str(e)})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
