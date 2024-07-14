from flask import Flask, request, jsonify
import json
import os
import google.generativeai as genai

app = Flask(__name__)

# load configuration
config_path = os.path.join(os.path.dirname(__file__), 'config.json')
with open(config_path, 'r') as file:
    config = json.load(file)

api_key = config['google_api_key']

# configure Generative AI
genai.configure(api_key=api_key)
model = genai.GenerativeModel(model_name='gemini-1.5-flash')

@app.route('/generate_content', methods=['POST'])
def generate_content():
    data = request.get_json()
    history = data.get('history')
    role = data.get('role', 'normal')
    answer_style = data.get('answer_style', 'short answer, less than 50 words')
    question = data.get('question', '')

    prompt = {
        'history': history,
        'role': role,
        'answer_style': answer_style,
        'question': question
    }

    prompt_json = json.dumps(prompt)
    response = model.generate_content(prompt_json)

    return jsonify({'content': response.text})

if __name__ == '__main__':
    app.run(debug=True)