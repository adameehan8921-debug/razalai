import os
import time
from flask import Flask, request, jsonify, render_template
from duckduckgo_search import DDGS

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


def fetch_results(query):
    results_list = []

    with DDGS() as ddgs:
        # 🔍 Normal search
        text_results = list(ddgs.text(query, max_results=15))

        # 📰 News search (extra quality)
        news_results = list(ddgs.news(query, max_results=5))

        combined = text_results + news_results

        seen_links = set()

        for r in combined:
            link = r.get("href", "")

            # ❌ skip duplicates
            if not link or link in seen_links:
                continue

            seen_links.add(link)

            title = r.get("title", "No title")
            snippet = r.get("body", "")

            # ❌ skip low-quality junk
            if len(snippet) < 30:
                continue

            results_list.append({
                "title": title,
                "snippet": snippet,
                "link": link
            })

    return results_list


@app.route('/search', methods=['POST'])
def search():
    try:
        data = request.get_json(force=True)
        query = data.get("query", "").strip()

        if not query:
            return jsonify({"error": "Empty query"}), 400

        results_list = []

        # 🔁 Retry system (important for Render stability)
        for attempt in range(3):
            try:
                results_list = fetch_results(query)

                if results_list:
                    break

            except Exception as e:
                print(f"Attempt {attempt+1} failed:", e)
                time.sleep(1)  # wait before retry

        if not results_list:
            return jsonify({"error": "No results found"}), 404

        return jsonify({
            "query": query,
            "results": results_list[:10]  # top 10 clean results
        })

    except Exception as e:
        print("Server Error:", e)
        return jsonify({"error": "Server error"}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
