import time

from flask import Flask, render_template, jsonify

app = Flask(__name__, template_folder='.')


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    #logic to implement to answer question of user
    time.sleep(1)
    return jsonify({'response': "hello"})

if __name__ == '__main__':
    app.run(debug=True)