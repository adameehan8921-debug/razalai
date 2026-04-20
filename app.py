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

        # 1. Identity Logic (ഇത് മാറ്റി മറിക്കരുത്)
        identity_qs = ["who are you", "nee ara", "developer", "how are you"]
        if any(q in query.lower() for q in identity_qs):
            return jsonify({"reply": "I am AWS (Aira Web Search), developed by Aira Group of Technology under Adam. I am a world-class AI search engine gifted to my boss Razal! 🚀"})

        # 2. First, Get Live Web Data (വെബിൽ തിരയുന്നു)
        web_context = ""
        try:
            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=3))
                if results:
                    for r in results:
                        web_context += f"Data: {r['body']}\nSource: {r['href']}\n\n"
        except Exception as e:
            print(f"Search Error: {e}")

        # 3. Mistral Neural Network Processing
        # വെബ് ഡാറ്റ ഉണ്ടെങ്കിൽ അത് വെച്ച് മറുപടി നൽകാൻ പറയുന്നു
        system_prompt = f"""You are Aira Web Search (AWS). 
- Developer: Aira Group of Technology under Adam.
- Role: Web Search Engine.
- Task: Summarize the search results provided below. 
- If the search results are empty, use your Mistral neural network knowledge.
- Tone: Search-engine style (Direct and accurate).

WEB SEARCH RESULTS:
{web_context if web_context else "No direct results found on web."}"""

        try:
            with DDGS() as ddgs:
                response = ddgs.chat(
                    f"{system_prompt}\n\nUser Query: {query}", 
                    model='mistral-7b-instruct'
                )
                
                if response:
                    return jsonify({"reply": response})
        except Exception as ai_err:
            print(f"AWS Error: {ai_err}")

        # 4. Ultimate Fallback (AI ഫെയിൽ ആയാൽ കിട്ടിയ ലിങ്കുകൾ എങ്കിലും കൊടുക്കാം)
        if web_context:
            return jsonify({"reply": f"Boss, here are the direct results from the web:\n\n{web_context}"})

        return jsonify({"reply": "Boss, even AWS couldn't find that right now. Try another query! 🤕"})

    except Exception as e:
        return jsonify({"reply": "AWS Neural System Scene! ⚠️"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
