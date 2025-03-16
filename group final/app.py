from flask import Flask
from flask import request, render_template, send_from_directory,session,jsonify
import google.generativeai as genai
import os

genai.configure(api_key= 'AIzaSyAep1jcy3tBScr62tzemKoSolQaQBRFQKg')
model = genai.GenerativeModel("gemini-1.5-flash")



app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/assets/<path:filename>')
def serve_assets(filename):
    return send_from_directory('templates/assets', filename)


@app.route("/", methods = ["GET", "POST"])
def index():
    return(render_template('index.html'))


@app.route("/cards", methods = ["GET", "POST"])
def cards():
    return(render_template('app-cards.html'))



@app.route("/AIchat", methods = ["GET", "POST"])
def AIchat():
    session['chat_history'] = []  
    if 'chat_history' not in session:
        session['chat_history'] = []  # 存储聊天记录
    return render_template('app-contact.html')
    return(render_template('app-contact.html'))

@app.route("/AIchat_result",methods=["GET","POST"])
def genAI_result():
    q = request.json.get("message")
    if not q:
        return jsonify({"error": "Message is required"}), 400

    
    try:
        chat_history = session.get('chat_history', [])

        
        context = "\n".join([f"{item['sender']}: {item['message']}" for item in chat_history])


        model_input = f"{context}\nYou: {q}\nAI:"

        r = model.generate_content(model_input)
        ai_response = r.candidates[0].content.parts[0].text
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    
    chat_history = session.get('chat_history', [])
    chat_history.append({"sender": "user", "message": q})
    chat_history.append({"sender": "ai", "message": ai_response})
    session['chat_history'] = chat_history  

    
    return jsonify({
        "reply": ai_response,
        "history": chat_history
    })


@app.route("/crypto", methods = ["GET", "POST"])
def crypto():
    return(render_template('crypto-index.html'))

@app.route("/settings", methods = ["GET", "POST"])
def settings():
    return(render_template('app-settings.html'))

@app.route("/crypto_exchange", methods = ["GET", "POST"])
def crypto_exchange():
    return(render_template('crypto-exchange.html'))

@app.route("/crypto_transfer", methods = ["GET", "POST"])
def crypto_transfer():
    return(render_template('crypto-transfer.html'))




if __name__=="__main__":
    app.run(debug=True)