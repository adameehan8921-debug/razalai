import os
from flask import Flask, request, jsonify, render_template
from duckduckgo_search import DDGS

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_data = request.json
        query = user_data.get("message", "").strip()

        if not query:
            return jsonify({"reply": "What should I search for, Boss? 🔍"}), 400

        search_data = ""
        sources = []

        # 🦆 DDGS search with error handling
        try:
            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=5))
                if results:
                    for r in results:
                        search_data += f"Source: {r['href']}\nSnippet: {r['body']}\n\n"
                        sources.append({"title": r['title'], "href": r['href']})
        except Exception as search_err:
            print(f"Search Error: {search_err}")
            search_data = "No live search results available at the moment."

        system_prompt = f"""You are Aira Web Search (AWS), a world-class AI search engine.
Developed by Adam (Aira Group) as a special gift for his best friend Razal.
Your ONLY bosses are Razal and Adam.
You MUST use the search results provided to answer.
Tone: Professional, loyal, and smart.
SEARCH RESULTS FROM WEB:
{search_data}"""

        # 🤖 Claude AI Chat
        try:
            with DDGS() as ddgs:
                response = ddgs.chat(
                    f"System: {system_prompt}\n\nUser Query: {query}",
                    model='claude-3-haiku'
                )
        except Exception as ai_err:
            print(f"AI Error: {ai_err}")
            return jsonify({"reply": "Boss, the AI brain is a bit tired. Try again! 🤕"})

        if response:
            return jsonify({"reply": response, "sources": sources})
        else:
            return jsonify({"reply": "Boss, I couldn't summarize the data. 🤕"})

    except Exception as e:
        print(f"Global Error: {e}")
        return jsonify({"reply": "AWS is facing a system scene! ⚠️"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
