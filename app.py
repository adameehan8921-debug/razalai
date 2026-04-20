import os
import time
from flask import Flask, request, jsonify, render_template
from duckduckgo_search import DDGS

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_data = request.get_json(force=True)
        query = user_data.get("message", "").strip()

        if not query:
            return jsonify({"reply": "What should I search for, Boss? 🔍"}), 400

        # 🧠 Identity Check
        identity_keywords = [
            "who are you", "nee ara", "developer",
            "who created you", "who made you"
        ]

        if any(keyword in query.lower() for keyword in identity_keywords):
            return jsonify({
                "reply": "👋 I am Aira Web Search (AWS)\n"
                         "🎁 Created by Adam as a special gift for my boss Razal\n"
                         "🚀 Fast • Smart • Reliable Web Search Engine"
            })

        results = []

        # 🔁 Retry system (Render stability)
        for attempt in range(3):
            try:
                with DDGS() as ddgs:
                    results = list(ddgs.text(
                        query,
                        max_results=6,
                        region="in-en",
                        safesearch="moderate"
                    ))

                if results:
                    break

            except Exception as e:
                print(f"Attempt {attempt+1} failed:", e)
                time.sleep(1)

        # ❌ No results fallback
        if not results:
            return jsonify({
                "reply": "Sorry Boss, I couldn't find strong results. Try another search 🔍",
                "sources": []
            })

        # 🧾 Clean formatting
        search_reply = "🔍 Boss, here’s what I found from the web:\n\n"
        clean_sources = []

        for i, r in enumerate(results, 1):
            title = r.get("title", "No title")
            snippet = r.get("body", "")
            link = r.get("href", "")

            if len(snippet) < 25:
                continue

            search_reply += f"{i}. {title}\n{snippet}\n\n"

            clean_sources.append({
                "title": title,
                "link": link
            })

        return jsonify({
            "reply": search_reply.strip(),
            "sources": clean_sources
        })

    except Exception as e:
        print(f"Search Error: {e}")
        return jsonify({
            "reply": "AWS Engine encountered a technical issue. ⚠️"
        })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
