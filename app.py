import os
import time
from flask import Flask, request, jsonify, render_template
from duckduckgo_search import DDGS

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


def is_identity(query):
    keywords = ["who are you", "nee ara", "developer", "who made you"]
    return any(k in query.lower() for k in keywords)


def is_question(query):
    q_words = ["who", "what", "when", "where", "why", "how", "aaranu", "entha"]
    return any(w in query.lower() for w in q_words)


def get_results(query):
    for attempt in range(3):
        try:
            with DDGS() as ddgs:
                return list(ddgs.text(query, max_results=6))
        except Exception as e:
            print(f"Retry {attempt+1}:", e)
            time.sleep(1)
    return []


@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json(force=True)
        query = data.get("message", "").strip()

        if not query:
            return jsonify({"reply": "Ask me something 🔍"}), 400

        # 🧠 Identity
        if is_identity(query):
            return jsonify({
                "reply": "👋 I am Aira Web Search (AWS)\n"
                         "🎁 A special gift for Razal\n"
                         "🚀 Smart • Fast • Web-powered"
            })

        results = get_results(query)

        if not results:
            return jsonify({
                "reply": "😕 No strong results found. Try again!"
            })

        clean_sources = []

        # 🧠 Smart Answer Mode
        if is_question(query):
            best = results[0]

            answer = best.get("body", "")
            title = best.get("title", "")
            link = best.get("href", "")

            reply = f"🧠 {answer}\n\n🔗 {title}"

            clean_sources.append({
                "title": title,
                "link": link
            })

        else:
            # 🔍 Search Mode
            reply = "🔍 Results:\n\n"

            for i, r in enumerate(results, 1):
                title = r.get("title", "")
                snippet = r.get("body", "")
                link = r.get("href", "")

                if len(snippet) < 25:
                    continue

                reply += f"{i}. {title}\n{snippet}\n\n"

                clean_sources.append({
                    "title": title,
                    "link": link
                })

        return jsonify({
            "reply": reply.strip(),
            "sources": clean_sources
        })

    except Exception as e:
        print("Error:", e)
        return jsonify({"reply": "⚠️ Something went wrong"})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
