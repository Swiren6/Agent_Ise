from flask import Flask, request, jsonify
from agent import SQLAssistant
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Active CORS pour toutes les routes

assistant = SQLAssistant()

@app.route('/ask', methods=['POST'])
def ask_question():
    data = request.get_json()
    question = data.get('question')
    
    if not question:
        return jsonify({"error": "Question is required"}), 400
    
    sql, response, cost, tokens = assistant.ask_question(question)
    
    return jsonify({
        "sql": sql,
        "response": response,
        "cost": cost,
        "tokens": tokens
    })

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)