from flask import Flask, render_template, request, jsonify
from google import genai
import json

app = Flask(__name__)

# !!! PASTE YOUR VALID GEMINI API KEY HERE !!!
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY_HERE"

try:
    client = genai.Client(api_key=GEMINI_API_KEY)
except Exception as e:
    print(f"Initialization Error: {e}")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate-story', methods=['POST'])
def generate_story():
    data = request.json
    user_prompt = data.get('prompt', '')

    if not user_prompt:
        return jsonify({'error': 'Please enter or select a story prompt'}), 400

    system_instruction = (
        "You are a kids comic writer. Respond ONLY with a raw JSON array of 4 objects. "
        "Do not wrap in markdown or backticks. JSON Keys must be: 'panel', 'visual_description', 'dialogue'."
    )
    
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=f"{system_instruction}\n\nConcept: {user_prompt}"
        )
        clean_text = response.text.replace("```json", "").replace("```", "").strip()
        comic_data = json.loads(clean_text)
        return jsonify({'comic': comic_data})
    except Exception as e:
        return jsonify({'error': f"API Error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
