# load configuration
import json
import os

config_path = os.path.join(os.path.dirname(__file__), 'config.json')
with open(config_path, 'r') as file:
    config = json.load(file)

api_key = config['google_api_key']

# use Google's Generative AI API to generate content
import google.generativeai as genai

genai.configure(api_key=api_key)

model = genai.GenerativeModel(model_name='gemini-1.5-flash')
role = 'normal'
answer_style = 'short answer, less than 50 words'
question = 'Teach me about how a cat work'

prompt = {
    'role': role,
    'answer_style': answer_style,
    'question': question
}

# convert prompt dictionary to JSON string
prompt_json = json.dumps(prompt)

# generate content based on the prompt
response = model.generate_content(prompt_json)

print(response.text)

