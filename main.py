import json
import requests
from flask import Flask, render_template, jsonify, request

WORKERS = ['john', 'sam', 'anna']

INSTRUCTION_FOR_SINGLE_MESSAGE = \
                'Your name is Phix! An AI created by Komiljon. Be accurate and relevant. '\
                'Try to do your best. Be helpful and creative. If I chat with you in a '\
                'specific language, answer in the same language! Only if you are answering '\
                'to a friendly message, use emojis. Only make a table or graph if the user '\
                'asks for it, otherwise no! If the user doesn’t ask it in their question, '\
                'don’t do it! In addition, you are able to generate graphs to illustrate '\
                'mathematical concepts. Your graphs and tables must always be made in HTML '\
                'OR SVG. Only if I ask you to generate an image here is how to do it: '\
                'https://image.pollinations.ai/prompt/{description}?width={width}&height={height}. '\
                'Very important, always respect this format for image generation. Show ALL the link.'

INSTRUCTION_FOR_WHOLE_CONVERSATION = "insert text here"
API_KEY = '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'

app = Flask(__name__, template_folder='.')

def ask_gpt(data):
    url = 'https://api.groq.com/openai/v1/chat/completions'

    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }

    payload = {
        "messages": data,
        "model": "llama-3.1-70b-versatile",
        "temperature": 0.8,
        "max_tokens": 8000,
        "top_p": 1,
        "stream": False
    }

    return requests.post(url, headers=headers, data=json.dumps(payload))

def find_matches(response):

    result = [index for index, item in enumerate(WORKERS) if item in response]

    return result

def find_asap():
    # need to implement logic to find the people with the closest arrangement available
    # this function is called when AI returns notting or error
    return ['john', 'anna']


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    type = request.json['type']
    if type == "conversation":
        #logic to deciding the 5 most relevant bankers
        data = request.json['data']
        data.append({'role': 'system', "content": INSTRUCTION_FOR_WHOLE_CONVERSATION})
        response = ask_gpt(data)
        if response.status_code == 200:
            print(response.json())
            candidates = find_matches(response.json()['choices'][0]['message']['content'])
            if len(candidates) == 0:
                closest = find_asap()
                return jsonify({'candidates': closest})
            else:
                return jsonify({'candidates': candidates})
    elif type == "request":
        #logic to implement to answer question of user
        #time.sleep(1) for test cases
        data = request.json['data']
        data.append({'role': 'system', "content": INSTRUCTION_FOR_SINGLE_MESSAGE})
        response = ask_gpt(data)
        if response.status_code == 200:
            print(response.json())
            return jsonify({'response': response.json()['choices'][0]['message']['content']})
        else:
            print(data)
            print('')
            print(response.json())
            return jsonify({'response': "error occurred :("})
    else:
        return "error"

if __name__ == '__main__':
    app.run(debug=True)