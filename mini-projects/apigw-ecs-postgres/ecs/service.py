import json

from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health():
    return 'Hello ECS Service'

@app.route('/countries', methods=['GET'])
def countries():
    with open('country-by-calling-code-v1.json') as f:
        data = json.load(f)
    return data

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)