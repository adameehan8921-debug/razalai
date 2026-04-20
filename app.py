import os
import requests
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_message = request.json.get("message", "").strip()
        
        if not user_message:
            return jsonify({"reply": "എന്താണ് സെർച്ച് ചെയ്യേണ്ടത് റസൽ ബോസ്സ്? 🔍"})

        # "Who are you" എന്ന ചോദ്യത്തിന് നിന്റെ സിസ്റ്റം പ്രോംപ്റ്റ് പ്രകാരം മറുപടി നൽകുന്നു
        identity_queries = ["who are you", "nee ara", "നിങ്ങൾ ആരാണ്", "njan ara"]
        if any(q in user_message.lower() for q in identity_queries):
            return jsonify({
                "reply": "ഞാൻ Aira Web Search (AWS). ആദം (Aira Group) ഉണ്ടാക്കി എന്റെ ബോസ്സായ റസലിന് സമ്മാനമായി നൽകിയതാണ് ഞാൻ! ഞാൻ ആണ് ലോകത്തെ മൂന്നാമത്തെ Ai based Search enginee 🤖🌐🚀"
            })

        # 🦆 DuckDuckGo Instant Answer API
        # ഇത് AI അല്ല, നേരിട്ട് വെബ് വിവരങ്ങൾ തരുന്ന സിസ്റ്റം ആണ്.
        ddg_url = f"https://api.duckduckgo.com/?q={user_message}&format=json&no_html=1"
        response = requests.get(ddg_url).json()

        # പ്രധാന വിവരങ്ങൾ ഉണ്ടോ എന്ന് നോക്കുന്നു
        answer = response.get('AbstractText')
        
        if not answer and response.get('RelatedTopics'):
            answer = response['RelatedTopics'][0].get('Text')

        if answer:
            final_reply = f"റസൽ ബോസ്സ്, ഇതാ വിവരം:\n\n{answer}\n\n— AWS Search"
        else:
            final_reply = "ക്ഷമിക്കണം ബോസ്സ്, വെബിൽ ഇതിനെക്കുറിച്ച് വ്യക്തമായ വിവരങ്ങൾ കിട്ടിയില്ല. 🤕"

        return jsonify({"reply": final_reply})

    except Exception as e:
        return jsonify({"reply": "AWS സിസ്റ്റത്തിൽ ചെറിയൊരു പിശക്! ⚠️"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
