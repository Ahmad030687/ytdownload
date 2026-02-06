from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
import random

app = Flask(__name__)

# ===============================
# 🛡️ SMART HEADERS (ANTI-BLOCK)
# ===============================
def get_headers():
    return {
        "User-Agent": random.choice([
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Mozilla/5.0 (Linux; Android 10)",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
        ]),
        "Accept": "text/html",
        "Referer": "https://www.google.com/"
    }

# ===============================
# 🏠 HOME
# ===============================
@app.route("/")
def home():
    return "🦅 AHMAD RDX ASK API LIVE"

# =================================================
# 🔍 ASK ENGINE (BING + DUCKDUCKGO)
# =================================================
@app.route("/api/ask", methods=["GET"])
def ask_engine():
    query = request.args.get("q", "").lower().strip()
    if not query:
        return jsonify({"status": False, "error": "Query missing"})

    # =========================
    # 🧠 INTENT DETECTION (FACT)
    # =========================
    if "pakistan" in query and ("kab bana" in query or "when was" in query or "founded" in query):
        return jsonify({
            "status": True,
            "question": query,
            "answer": "Pakistan 14 August 1947 ko bana tha.",
            "language": "roman_urdu",
            "brand": "AHMAD RDX"
        })

    # =========================
    # 🔍 SEARCH MODE (GENERAL)
    # =========================
    q = quote_plus(query)
    results = []

    try:
        r = requests.get(
            f"https://www.bing.com/search?q={q}",
            headers=get_headers(),
            timeout=10
        )
        soup = BeautifulSoup(r.text, "html.parser")

        for item in soup.select("li.b_algo")[:5]:
            title = item.select_one("h2")
            link = item.select_one("a")
            desc = item.select_one(".b_caption p")

            if title and link:
                results.append({
                    "title": title.get_text(strip=True),
                    "link": link.get("href"),
                    "description": desc.get_text(strip=True) if desc else ""
                })
    except:
        pass

    if not results:
        return jsonify({
            "status": False,
            "answer": "Is sawal ka reliable jawab nahi mila.",
            "language": "roman_urdu",
            "brand": "AHMAD RDX"
        })

    # Roman Urdu fallback (simple)
    answer = results[0]["description"] or results[0]["title"]

    return jsonify({
        "status": True,
        "question": query,
        "answer": f"Mukhtasir jawab: {answer}",
        "language": "mixed",
        "brand": "AHMAD RDX"
    })
    short_answer = results[0]["description"] or results[0]["title"]

    return jsonify({
        "status": True,
        "question": query,
        "answer": short_answer,
        "results": results,
        "brand": "AHMAD RDX"
    })

# ===============================
# 🚀 RUN
# ===============================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
