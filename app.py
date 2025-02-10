# --------- imports
from flask import Flask, render_template, request, jsonify
import os
import requests

app = Flask(__name__)

# Load the API key from environment variables
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    raise ValueError("No Gemini API key found. Please set the GEMINI_API_KEY environment variable.")
API_URL = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={}'.format(GEMINI_API_KEY)

# Routes
@app.route('/')
def home():
    return render_template('chat.html')

@app.route('/message', methods=['POST'])
def message():
    user_msg = request.form['message']

    # Send user message to Gemini
    response = requests.post(
        API_URL,
        json={
            "contents": [{"role": "user", "parts": [{"text": user_msg}]}],
            "temperature": 0.1,
            "candidateCount": 1,
            "safetySettings": [
                { "category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE" },
                { "category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE" }
            ]
        }
    )

    if response.status_code == 200:
        ai_response = response.json()['candidates'][0]['content']['parts'][0]['text']
        return jsonify({'ai_reply': ai_response})
    else:
        return jsonify({'error': 'API request failed'}), 500

if __name__ == '__main__':
    app.run(debug=True)