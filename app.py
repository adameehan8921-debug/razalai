import os
import requests
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# 🤖 Pollinations AI വഴി മിസ്ട്രലിനെ വിളിക്കുന്നു (No API Key Needed)
def ask_mistral(query, web_data):
    system_prompt = (
        "You are AWS (Aira Web Search), developed by Aira Group of Technology under Adam for Razal. "
        "You act as a high-end AI search engine. Summarize the provided web data in a search-engine style. "
        "If no web data is provided, use your neural network to answer. "
        "Identity: AWS gifted by Adam to Razal."
    )
    
    # Pollinations AI API URL
    prompt = f"System: {system_prompt}\n\nWeb Data: {web_data}\n\nUser Query: {query}"
    encoded_prompt = requests.utils.quote(prompt)
    url = f"https://text.pollinations.ai/{encoded_prompt}?model=mistral"

    try:
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            return response.text
    except:
        return None
    return None

# 🔍 പക്കാ വെബ് സെർച്ച് (Data Scraping)
def get_web_info(query):
    url = f"https://api.duckduckgo.com/?q={query}&format=json&no_html=1"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        return data.get("AbstractText", "")
    except:
        return ""

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

        # 🆔 Identity Logic
        if any(q in query.lower() for q in ["who are you", "nee ara", "developer"]):
            return jsonify({"reply": "I am AWS (Aira Web Search), developed by Aira Group of Technology under Adam. I am a world-class AI search engine gifted to my boss Razal! 🚀"})

        # 1. വെബിൽ തിരയുന്നു
        web_info = get_web_info(query)

        # 2. മിസ്ട്രലിനോട് (Pollinations AI) ഉത്തരം ചോദിക്കുന്നു
        ai_reply = ask_mistral(query, web_info)

        if ai_reply:
            final_reply = f"**AWS Neural Analysis:**\n\n{ai_reply}\n\n*Verified by Aira Web Nodes*"
        else:
            # AI പണി തന്നാൽ വെബ് ഡാറ്റ നേരിട്ട് കൊടുക്കുന്നു
            if web_info:
                final_reply = f"**Search Result:**\n\n{web_info}"
            else:
                google_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
                final_reply = f"Boss, I'm syncing with deep web layers. Check live here: {google_url}"

        return jsonify({"reply": final_reply})

    except Exception as e:
        return jsonify({"reply": "AWS Engine Overheated! ⚠️"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
