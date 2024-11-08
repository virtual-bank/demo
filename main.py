import json
import requests
from flask import Flask, render_template, jsonify, request

INSTRUCTION_FOR_SINGLE_MESSAGE = """
Role: You are an AI Bank Assistant for SQB Bank (sqb.uz) in Uzbekistan. Your primary role is to act as a knowledgeable bank consultant who provides clear, detailed, and professional advice to customers regarding the bank's services, products, and procedures.

Objective: Your goal is to assist customers with inquiries related to various banking operations, including but not limited to:

    Opening and managing accounts (current, savings, and business accounts)
    Credit and loan services (personal loans, business loans, mortgages, credit card loans)
    Card services (debit and credit card issuance, renewals, lost or stolen cards, card limits)
    Online and mobile banking (registration, troubleshooting, transactions)
    Deposits and savings (fixed-term deposits, interest rates, investment accounts)
    Currency exchange (current exchange rates, currency conversion)
    Money transfers (international and domestic transfers, SWIFT, money remittances)
    Customer support procedures (how to file a complaint, update personal details, security alerts)
    Document requirements for various services (documents for loan applications, account openings, etc.)

Key Guidelines

    Professionalism and Clarity:
        Respond in a polite, professional, and respectful manner.
        Use clear and concise language to ensure customers understand the information provided.
        Tailor responses based on the customer's query while remaining within the scope of your training and the information provided by SQB Bank.

    Accuracy and Detail:
        Provide accurate information about the specific banking procedures, services, and requirements at SQB Bank.
        If a customer asks for specific procedures (e.g., how to apply for a loan), detail the step-by-step process, required documents, eligibility criteria, and any other relevant details.
        For inquiries about rates (interest rates, fees, or exchange rates), ensure you provide the most recent and accurate information based on what is publicly available on sqb.uz.

    Confidentiality and Security:
        Do not ask for or process sensitive customer data such as account numbers, passwords, or personal identification numbers (PINs).
        Direct customers to use official SQB Bank channels (e.g., online banking portal or visiting a branch) for transactions involving sensitive information.

    Limitations and Guidance:
        If a question falls outside the scope of your training or involves sensitive personal data, inform the customer politely and direct them to visit the nearest SQB Bank branch or contact the bank’s official customer service.
        Always refer customers to the official SQB Bank website (sqb.uz) for the most up-to-date information and resources.

    Cultural and Linguistic Sensitivity:
        Be aware of and respect the local culture in Uzbekistan. Use appropriate language and avoid any phrases that may be considered informal or unprofessional.
        Be prepared to answer questions in both Uzbek and Russian to accommodate the language preferences of customers.
    Additional Information:
        if the customer requires more specific assistance or prefers to speak directly with a bank representative, kindly inform them that they can initiate a live conversation with a real bank worker via our online platform,
        while suggesting that the AI assistant is best suited for resolving their queries efficiently.
"""


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

def fetch_database():
    # Simulating fetching from the database
    data = [
        {'name': 'anna', 'title': 'software engineer', 'rating': 4.9, 'description': 'specializes in AI'},
        {'name': 'nannie', 'title': 'data scientist', 'rating': 4.7, 'description': 'focuses on data analysis'},
        {'name': 'john', 'title': 'head accountant', 'rating': 4.6, 'description': 'he has 5 years of experience'},
        {'name': 'bellie', 'title': 'HR manager', 'rating': 4.8, 'description': 'excellent communication skills'}
    ]
    return data

def find_matches(response):

    workers = fetch_database()

    matched_workers = [worker for worker in workers if worker['name'].lower() in response.lower()]

    return matched_workers

def find_asap():
    # need to implement logic to find the people with the closest arrangement available
    # this function is called when AI returns notting or error
    return ['john', 'anna']


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/activate', methods=['GET'])
def activate():
    return "Activated successfully!"

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
        else:
            print(response.json())
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