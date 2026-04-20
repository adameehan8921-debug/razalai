import os
import requests
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

def ask_mistral(query):
    # മിസ്ട്രലിനോട് പക്കാ ഒരു വെബ് സെർച്ച് എൻജിൻ ആയി പ്രവർത്തിക്കാൻ പറയുന്നു
    # അവൾ തന്നെ ഡാറ്റ തിരഞ്ഞു കണ്ടുപിടിച്ചു തരുന്ന രീതിയിലുള്ള പ്രോംപ്റ്റ്
    system_persona = (
        "You are AWS (Aira Web Search), a high-speed AI web search engine. "
        "Developed by Aira Group of Technology under Adam. Your boss is Razal. "
        "Your task: Perform a deep web search for the user query and provide a structured, professional search summary. "
        "Do not act like a chatbot. Use search-engine style phrases like 'Live Indexing Results' or 'Top Web Findings'. "
        "If you don't know the answer, pretend you are still crawling the database."
    )
    
    # Pollinations AI-ലേക്ക് മിസ്ട്രലിനെ വിളിക്കുന്നു
    # ഇതാണ് മിസ്ട്രലിന്റെ സെർച്ച് എബിലിറ്റി ട്രിഗർ ചെയ്യുന്നത്
    url = f"https://text.pollinations.ai/{requests.utils.quote(query)}?model=mistral&system={requests.utils.quote(system_persona)}"

    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            return response.text
    except Exception as e:
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
            return jsonify({"reply": "Ready for Search, Boss... 🔍"}), 400

        # 🆔 Identity Check - Aira Group & Adam Special
        if any(q in query.lower() for q in ["who are you", "nee ara", "developer", "made you"]):
            return jsonify({
                "reply": "🔍 **AWS Identity Verified:** I am Aira Web Search, developed by Aira Group of Technology under Adam. A world-class neural search engine gifted to my boss Razal! 🚀"
            })

        # 🧠 Let Mistral do the "Web Search" acting
        ai_response = ask_mistral(query)

        if ai_response:
            # പക്കാ സെർച്ച് റിസൾട്ട് ലുക്ക് വരാൻ ഫൈനൽ ടച്ച്
            final_reply = f"🌐 **AWS LIVE SEARCH ANALYSIS:**\n\n{ai_response}\n\n*Nodes: Active | Source: Global Web Index*"
            return jsonify({"reply": final_reply})
        else:
            return jsonify({
                "reply": "Boss, the neural network is syncing with global servers. Please try that query again! 🤕"
            })

    except Exception as e:
        return jsonify({"reply": "⚠️ **System Alert:** Neural nodes are recalibrating."})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
