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
    query = request.args.get("q", "").strip()
    if not query:
        return jsonify({
            "status": False,
            "error": "Query missing"
        })

    q = quote_plus(query)
    results = []

    # -------- BING SEARCH --------
    try:
        bing_url = f"https://www.bing.com/search?q={q}"
        r = requests.get(bing_url, headers=get_headers(), timeout=10)
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
    except Exception as e:
        print("BING ERROR:", e)

    # -------- DUCKDUCKGO FALLBACK --------
    if not results:
        try:
            ddg_url = f"https://duckduckgo.com/html/?q={q}"
            r = requests.get(ddg_url, headers=get_headers(), timeout=10)
            soup = BeautifulSoup(r.text, "html.parser")

            for item in soup.select(".result")[:5]:
                a = item.select_one(".result__a")
                s = item.select_one(".result__snippet")

                if a:
                    results.append({
                        "title": a.get_text(strip=True),
                        "link": a.get("href"),
                        "description": s.get_text(strip=True) if s else ""
                    })
        except Exception as e:
            print("DDG ERROR:", e)

    # -------- FINAL RESPONSE --------
    if not results:
        return jsonify({
            "status": False,
            "answer": "No reliable result found",
            "results": [],
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
