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


INSTRUCTION_FOR_WHOLE_CONVERSATION = """Given the following array of bank workers with their name, title, rating, description, and availability, please provide a list of the top 5 most suitable bank workers, ordered by the following criteria:
1. Most recent availability time.
2. Highest rating.
3. Specialization or area of expertise (prioritize workers with expertise relevant to a customer's needs).

The array of workers is as follows:

data = [
        {'name': 'john', 'title': 'relationship manager', 'rating': 4.8,
         'description': 'specializes in personal banking and customer relationships', "available": "11/09/2024 14:30"},
        {'name': 'anna', 'title': 'loan officer', 'rating': 4.7,
         'description': 'focused on mortgage and personal loans', "available": "11/10/2024 09:45"},
        {'name': 'emily', 'title': 'investment consultant', 'rating': 4.9,
         'description': 'provides investment advice and portfolio management', "available": "11/11/2024 13:00"},
        {'name': 'michael', 'title': 'financial planner', 'rating': 4.6,
         'description': 'specializes in retirement planning and wealth management', "available": "11/13/2024 15:30"},
        {'name': 'susan', 'title': 'credit analyst', 'rating': 4.7,
         'description': 'focuses on analyzing creditworthiness for loans', "available": "11/09/2024 11:00"},
        {'name': 'paul', 'title': 'commercial banker', 'rating': 4.8,
         'description': 'expert in business loans and financial services', "available": "11/12/2024 16:00"},
        {'name': 'tina', 'title': 'wealth advisor', 'rating': 4.9,
         'description': 'focuses on high-net-worth individual clients', "available": "11/14/2024 10:15"},
        {'name': 'roger', 'title': 'mortgage consultant', 'rating': 4.7,
         'description': 'specializes in helping clients with home financing options', "available": "11/15/2024 12:30"},
        {'name': 'grace', 'title': 'risk manager', 'rating': 4.6,
         'description': 'works on identifying and managing financial risks', "available": "11/08/2024 14:00"},
        {'name': 'ben', 'title': 'operations manager', 'rating': 4.8,
         'description': 'oversees bank operations and ensures efficiency', "available": "11/09/2024 17:30"},
        {'name': 'lily', 'title': 'banking consultant', 'rating': 4.7,
         'description': 'advises clients on banking products and services', "available": "11/11/2024 10:30"},
        {'name': 'nathan', 'title': 'foreign exchange consultant', 'rating': 4.9,
         'description': 'specializes in foreign currency exchange and international transactions',
         "available": "11/10/2024 13:00"},
        {'name': 'sophie', 'title': 'digital banking consultant', 'rating': 4.6,
         'description': 'helps clients with digital banking tools and services', "available": "11/14/2024 09:00"},
        {'name': 'harry', 'title': 'small business banker', 'rating': 4.8,
         'description': 'provides financial solutions to small and medium-sized enterprises',
         "available": "11/12/2024 16:30"},
        {'name': 'jessica', 'title': 'compliance officer', 'rating': 4.7,
         'description': 'ensures banking activities comply with regulations', "available": "11/09/2024 13:00"},
        {'name': 'will', 'title': 'payment systems consultant', 'rating': 4.9,
         'description': 'specializes in payment processing and security', "available": "11/08/2024 11:00"},
        {'name': 'claire', 'title': 'customer service representative', 'rating': 4.6,
         'description': 'provides assistance with accounts and services', "available": "11/11/2024 14:00"},
        {'name': 'david', 'title': 'financial analyst', 'rating': 4.8,
         'description': 'analyzes market trends to advise on investment opportunities',
         "available": "11/13/2024 12:30"},
        {'name': 'olivia', 'title': 'bank branch manager', 'rating': 4.7,
         'description': 'manages day-to-day operations and staff of a bank branch', "available": "11/14/2024 15:00"}
    ]

Please send the top 5 suitable workers' name only based on the criteria above."""

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
        {'name': 'john', 'title': 'relationship manager', 'rating': 4.8,
         'description': 'specializes in personal banking and customer relationships', "available": "11/09/2024 14:30"},
        {'name': 'anna', 'title': 'loan officer', 'rating': 4.7,
         'description': 'focused on mortgage and personal loans', "available": "11/10/2024 09:45"},
        {'name': 'emily', 'title': 'investment consultant', 'rating': 4.9,
         'description': 'provides investment advice and portfolio management', "available": "11/11/2024 13:00"},
        {'name': 'michael', 'title': 'financial planner', 'rating': 4.6,
         'description': 'specializes in retirement planning and wealth management', "available": "11/13/2024 15:30"},
        {'name': 'susan', 'title': 'credit analyst', 'rating': 4.7,
         'description': 'focuses on analyzing creditworthiness for loans', "available": "11/09/2024 11:00"},
        {'name': 'paul', 'title': 'commercial banker', 'rating': 4.8,
         'description': 'expert in business loans and financial services', "available": "11/12/2024 16:00"},
        {'name': 'tina', 'title': 'wealth advisor', 'rating': 4.9,
         'description': 'focuses on high-net-worth individual clients', "available": "11/14/2024 10:15"},
        {'name': 'roger', 'title': 'mortgage consultant', 'rating': 4.7,
         'description': 'specializes in helping clients with home financing options', "available": "11/15/2024 12:30"},
        {'name': 'grace', 'title': 'risk manager', 'rating': 4.6,
         'description': 'works on identifying and managing financial risks', "available": "11/08/2024 14:00"},
        {'name': 'ben', 'title': 'operations manager', 'rating': 4.8,
         'description': 'oversees bank operations and ensures efficiency', "available": "11/09/2024 17:30"},
        {'name': 'lily', 'title': 'banking consultant', 'rating': 4.7,
         'description': 'advises clients on banking products and services', "available": "11/11/2024 10:30"},
        {'name': 'nathan', 'title': 'foreign exchange consultant', 'rating': 4.9,
         'description': 'specializes in foreign currency exchange and international transactions',
         "available": "11/10/2024 13:00"},
        {'name': 'sophie', 'title': 'digital banking consultant', 'rating': 4.6,
         'description': 'helps clients with digital banking tools and services', "available": "11/14/2024 09:00"},
        {'name': 'harry', 'title': 'small business banker', 'rating': 4.8,
         'description': 'provides financial solutions to small and medium-sized enterprises',
         "available": "11/12/2024 16:30"},
        {'name': 'jessica', 'title': 'compliance officer', 'rating': 4.7,
         'description': 'ensures banking activities comply with regulations', "available": "11/09/2024 13:00"},
        {'name': 'will', 'title': 'payment systems consultant', 'rating': 4.9,
         'description': 'specializes in payment processing and security', "available": "11/08/2024 11:00"},
        {'name': 'claire', 'title': 'customer service representative', 'rating': 4.6,
         'description': 'provides assistance with accounts and services', "available": "11/11/2024 14:00"},
        {'name': 'david', 'title': 'financial analyst', 'rating': 4.8,
         'description': 'analyzes market trends to advise on investment opportunities',
         "available": "11/13/2024 12:30"},
        {'name': 'olivia', 'title': 'bank branch manager', 'rating': 4.7,
         'description': 'manages day-to-day operations and staff of a bank branch', "available": "11/14/2024 15:00"}
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

@app.route('/booking', methods=['GET'])
def book():
    return render_template('book.html')

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
                print(candidates)
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