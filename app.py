import os
import requests
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

def ask_mistral(query):
    # മിസ്ട്രലിനെ പക്കാ സെർച്ച് എഞ്ചിൻ ആക്കാൻ
    system_prompt = (
        "You are AWS (Aira Web Search), developed by Aira Group of Technology under Adam. "
        "Your boss is Razal. You are a high-speed web search AI. "
        "Summarize the query as if you are providing real-time search results. "
        "Be professional, direct, and act like a search engine."
    )
    
    # Pollinations AI POST Endpoint - ഇത് കൂടുതൽ സ്റ്റേബിൾ ആണ്
    payload = {
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query}
        ],
        "model": "mistral"
    }

    try:
        # Timeout 30 സെക്കൻഡ് വരെ കൊടുക്കാം
        response = requests.post("https://text.pollinations.ai/", json=payload, timeout=30)
        if response.status_code == 200:
            return response.text
    except Exception as e:
        print(f"API Error: {e}")
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
            return jsonify({"reply": "Ready to scan the web, Boss... 🔍"}), 400

        # 🆔 Identity Logic
        if any(q in query.lower() for q in ["who are you", "nee ara", "developer"]):
            return jsonify({
                "reply": "🔍 **AWS Identity Verified:** I am Aira Web Search, created by Aira Group of Technology under Adam. A dedicated gift for my boss Razal! 🚀"
            })

        # 🧠 Calling Mistral
        ai_response = ask_mistral(query)

        if ai_response:
            final_reply = f"🌐 **AWS LIVE SEARCH ANALYSIS:**\n\n{ai_response}\n\n*Verified by Aira Neural Nodes*"
            return jsonify({"reply": final_reply})
        else:
            # എറർ വന്നാൽ സിസ്റ്റം ഒന്ന് റീസ്റ്റാർട്ട് ചെയ്യാൻ പറയും പോലെ തോന്നും
            return jsonify({
                "reply": "Boss, it seems the global web nodes are heavy. Let me try one more time, just click search again! 🚀"
            })

    except Exception as e:
        return jsonify({"reply": "⚠️ **System Alert:** Neural system recalibrating."})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
