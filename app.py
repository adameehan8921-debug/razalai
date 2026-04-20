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

        # 1. 🆔 Identity Check - Mistral acting as AWS
        identity_qs = ["who are you", "nee ara", "developer", "made you", "created you"]
        if any(q in query.lower() for q in identity_qs):
            return jsonify({
                "reply": "I am AWS (Aira Web Search), a world-class AI search engine developed by Aira Group of Technology under Adam. I am a dedicated neural-search gift for my boss Razal! 🚀"
            })

        # 2. 🧠 Mistral Roleplay as Web Search AI
        # മിസ്ട്രലിനോട് ഒരു സെർച്ച് എൻജിൻ ആയിട്ട് അഭിനയിക്കാൻ നമ്മൾ നിർദ്ദേശം നൽകുന്നു
        system_instructions = (
            "You are AWS (Aira Web Search), a high-end AI search engine. "
            "Your developer is Aira Group of Technology under Adam. "
            "Your boss is Razal. "
            "IMPORTANT: Do not act like a chatbot. Act like a search engine's intelligence. "
            "When a user asks a question, analyze it and provide a direct search-result style summary. "
            "Use your Mistral-7B neural network to process information but keep the persona of a web search agent."
        )

        try:
            with DDGS() as ddgs:
                # മിസ്ട്രലിനെ ഇവിടെ വിളിക്കുന്നു
                response = ddgs.chat(
                    f"Instruction: {system_instructions}\n\nQuery: {query}", 
                    model='mistral-7b-instruct'
                )
                
                if response:
                    # മറുപടിയിൽ ഒരു സെർച്ച് എൻജിൻ ടച്ച് നൽകുന്നു
                    final_reply = f"**AWS Neural Analysis:**\n\n{response}\n\n*Verified by Aira Web Nodes*"
                    return jsonify({"reply": final_reply})
        
        except Exception as ai_err:
            print(f"AI Error: {ai_err}")

        # 3. 🦆 Fallback (AI പണി തന്നാൽ പച്ചയായ വെബ് ഡാറ്റ)
        try:
            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=3))
                if results:
                    fallback_reply = "Boss, I've bypassed the neural nodes and fetched direct web results:\n\n"
                    for r in results:
                        fallback_reply += f"🔍 {r['title']}\n{r['body']}\n\n"
                    return jsonify({"reply": fallback_reply})
        except:
            pass

        return jsonify({"reply": "Boss, the neural network is currently re-indexing. Please try again! 🤕"})

    except Exception as e:
        return jsonify({"reply": "AWS Engine Overheated! ⚠️"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
