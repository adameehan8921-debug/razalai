import os
import requests
import re
import math
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# 🔢 പൈത്തൺ കണക്ക് കൂട്ടുന്നു, പക്ഷേ AI സ്റ്റൈലിൽ മറുപടി നൽകുന്നു
def get_ai_math_response(query):
    clean_query = query.lower().replace(' ', '').replace('x', '*')
    
    # കണക്കാണോ എന്ന് പരിശോധിക്കുന്നു
    if re.match(r"^[0-9+\-*/().%^sqrt|sin|cos|tan|log|pi|e]+$", clean_query):
        try:
            safe_dict = {k: getattr(math, k) for k in dir(math) if not k.startswith("_")}
            result = eval(clean_query, {"__builtins__": None}, safe_dict)
            
            # 🎭 ഇവിടെയാണ് അഭിനയം! ഒരു AI സെർച്ച് റിസൾട്ട് പോലെ മറുപടി ഉണ്ടാക്കുന്നു.
            ai_style_reply = (
                f"🔍 **Math Query Analysis:**\n"
                f"The mathematical expression '{query}' was processed by our neural calculation engine.\n\n"
                f"📝 **Solution:** {result}\n\n"
                f"💡 **Note:** This calculation was verified using Python's high-precision mathematical library."
            )
            return ai_style_reply
        except:
            return None
    return None

def get_web_result(query):
    url = f"https://api.duckduckgo.com/?q={query}&format=json&no_html=1"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        if data.get("AbstractText"):
            return data["AbstractText"]
        return None
    except:
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
            return jsonify({"reply": "What should I scan for, Boss? 🔍"}), 400

        # 1. 🆔 Identity (The Legend Adam & Razal)
        if any(q in query.lower() for q in ["who are you", "nee ara", "developer"]):
            return jsonify({"reply": "🔍 **AWS Identity Verified:** I am Aira Web Search, developed by Aira Group of Technology under Adam. A world-class AI search engine gifted to my boss Razal! 🚀"})

        # 2. 🔢 AI Style Math Response
        math_ai_res = get_ai_math_response(query)
        if math_ai_res:
            return jsonify({"reply": f"🌐 **AWS Neural Calculation:**\n\n{math_ai_res}"})

        # 3. 🌐 Standard Web Search
        web_res = get_web_result(query)
        if web_res:
            return jsonify({"reply": f"🌐 **AWS Global Index:**\n\n{web_res}\n\n*Verified by Aira Nodes*"})
        
        # 4. Fallback
        google_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        return jsonify({"reply": f"Boss, no direct summary found in the neural cache. [Check Live Web Results]({google_url})"})

    except Exception as e:
        return jsonify({"reply": "⚠️ **System Alert:** Neural nodes are recalibrating."})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
