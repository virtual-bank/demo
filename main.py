import time

from flask import Flask, render_template, jsonify, request

app = Flask(__name__, template_folder='.')


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    type = request.json['type']
    if type == "conversation":
        #logic to deciding the 5 most relevant bankers
        print(request.json['data'])
        return "ok"
    elif type == "response":
        #logic to implement to answer question of user
        time.sleep(1)
        return jsonify({'response': "hello"})
    else:
        return "error"

if __name__ == '__main__':
    app.run(debug=True)