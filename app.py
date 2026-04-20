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

        # 1. 🦆 പച്ചയായ വെബ് സെർച്ച് ആദ്യം നടത്തുന്നു
        search_data = ""
        sources = []
        with DDGS() as ddgs:
            # ലോകത്തെവിടെ നിന്നുള്ള ലേറ്റസ്റ്റ് ഡാറ്റയും സെർച്ച് ചെയ്യുന്നു
            results = list(ddgs.text(query, max_results=5))
            if results:
                for r in results:
                    search_data += f"Source: {r['href']}\nSnippet: {r['body']}\n\n"
                    sources.append({"title": r['title'], "href": r['href']})

        # 2. 🔥 RAZAL SPECIAL SYSTEM PROMPT + CLAUDE INTELLIGENCE
        # സെർച്ച് ഡാറ്റ ഉണ്ടെങ്കിൽ അത് വെച്ച് മറുപടി നൽകാൻ ക്ലോഡിനോട് പറയുന്നു
        system_prompt = f"""You are Aira Web Search (AWS), a world-class AI search engine.
- Developed by Adam (Aira Group) as a special gift for his best friend Razal.
- Your ONLY boss is Razal and Adam.
- You MUST use the search results provided below to answer. If the data is not there, use your internal knowledge but keep the search engine style.
- Tone: Professional, loyal, and smart. 
- Identity: If asked who you are, say you are AWS gifted by Adam to Razal.

SEARCH RESULTS FROM WEB:
{search_data}"""

        # 3. 🤖 Claude AI വഴി സെർച്ച് റിസൾട്ട് മിനുക്കിയെടുക്കുന്നു
        with DDGS() as ddgs:
            response = ddgs.chat(
                f"User Query: {query}\n\nBased on the search results, provide a detailed answer for Razal.",
                model='claude-3-haiku'
            )
            
        if response:
            return jsonify({
                "reply": response,
                "sources": sources # വെബ്സൈറ്റ് ലിങ്കുകൾ താഴെ കാണിക്കാൻ
            })
        else:
            return jsonify({"reply": "Boss, I searched the web but couldn't summarize the data. 🤕"})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"reply": "AWS Engine encountered a technical glitch. ⚠️"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
