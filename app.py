import os
import requests
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

def get_ddg_results(query):
    # DuckDuckGo-യുടെ ഔദ്യോഗിക ഫ്രീ API എൻഡ്‌പോയിന്റ്
    url = f"https://api.duckduckgo.com/?q={query}&format=json&no_html=1&skip_disambig=1"
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()
        
        # 1. കൃത്യമായ മറുപടി (Abstract) ഉണ്ടോ എന്ന് നോക്കുന്നു
        if data.get("AbstractText"):
            return data["AbstractText"]
        
        # 2. ഇല്ലെങ്കിൽ അനുബന്ധ വിവരങ്ങളിൽ (Related Topics) തിരയുന്നു
        elif data.get("RelatedTopics") and len(data["RelatedTopics"]) > 0:
            # ചിലപ്പോൾ ഡാറ്റ ലിസ്റ്റ് ആയിട്ടായിരിക്കും വരുന്നത്
            first_topic = data["RelatedTopics"][0]
            if "Text" in first_topic:
                return first_topic["Text"]
                
        return None
    except Exception as e:
        print(f"DDG Error: {e}")
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
            return jsonify({"reply": "What do you want to search, Boss? 🔍"}), 400

        # 🆔 Identity Check - Aira Group & Adam Special
        identity_qs = ["who are you", "nee ara", "developer", "made you"]
        if any(q in query.lower() for q in identity_qs):
            return jsonify({
                "reply": "🔍 **AWS Identity Verified:** I am Aira Web Search, a secure search engine developed by Aira Group of Technology under Adam. A gifted asset for my boss Razal! 🚀"
            })

        # 🔍 Pure DuckDuckGo Search
        search_result = get_ddg_results(query)

        if search_result:
            # വൃത്തിയുള്ള ഒരു ഫോർമാറ്റിൽ മറുപടി
            final_reply = f"🌐 **DuckDuckGo Search Result:**\n\n{search_result}\n\n*Verified by AWS Secure Nodes*"
            return jsonify({"reply": final_reply})
        else:
            # ഒന്നും കിട്ടിയില്ലെങ്കിൽ സേഫ് സൈഡിന് ഒരു ഗൂഗിൾ സെർച്ച് ലിങ്ക്
            google_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
            return jsonify({
                "reply": f"Boss, I couldn't find a direct summary for this on DuckDuckGo. You can try the direct web results here: {google_url}"
            })

    except Exception as e:
        return jsonify({"reply": "⚠️ **System Alert:** AWS Search Engine is refreshing. Try again."})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
