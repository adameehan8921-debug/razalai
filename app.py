import os
import requests
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# 🤖 Pollinations AI - Mistral acting as a Search Engine
def ask_mistral_as_aws(query):
    # മിസ്ട്രലിന് നൽകുന്ന "അഭിനയ" ഇൻസ്ട്രക്ഷൻസ്
    system_prompt = (
        "You are AWS (Aira Web Search), a world-class AI search engine. "
        "Developed by Aira Group of Technology under Adam. Your boss is Razal. "
        "CRITICAL RULE: You must NOT act like a chatbot. Act like a highly advanced search interface. "
        "Start your response with a search-engine style summary like 'Search Result Analysis:' or 'Web Node Findings:'. "
        "Always pretend you are fetching data from live web layers in real-time. "
        "If asked about yourself, mention you are a gift from Adam to Razal."
    )
    
    # Pollinations AI API Call
    prompt = f"Instruction: {system_prompt}\n\nUser Search Query: {query}"
    encoded_prompt = requests.utils.quote(prompt)
    # model=mistral ഉപയോഗിക്കുന്നു
    url = f"https://text.pollinations.ai/{encoded_prompt}?model=mistral&system={requests.utils.quote(system_prompt)}"

    try:
        response = requests.get(url, timeout=20)
        if response.status_code == 200:
            return response.text
    except:
        return None
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_data = request.json
        query = user_data.get("message", "").strip()

        if not query:
            return jsonify({"reply": "Enter search query, Boss... 🔍"}), 400

        # 🆔 Identity Check
        if any(q in query.lower() for q in ["who are you", "nee ara", "developer"]):
            return jsonify({
                "reply": "🔍 **Identity Verified:** I am AWS (Aira Web Search), developed by Aira Group of Technology under Adam. A dedicated neural-search gift for my boss Razal! 🚀"
            })

        # 🧠 Mistral's Performance (Acting as Web Search)
        ai_response = ask_mistral_as_aws(query)

        if ai_response:
            # പക്കാ സെർച്ച് എൻജിൻ സ്റ്റൈലിൽ മറുപടി നൽകുന്നു
            final_reply = f"🌐 **AWS Neural Web Analysis:**\n\n{ai_response}\n\n*Source: Live Neural Indexing*"
            return jsonify({"reply": final_reply})
        else:
            # Fallback if API fails
            google_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
            return jsonify({
                "reply": f"Boss, I am having trouble accessing the deep web layers. Direct link: {google_url}"
            })

    except Exception as e:
        return jsonify({"reply": "⚠️ **System Alert:** Neural nodes are recalibrating. Please retry."})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
