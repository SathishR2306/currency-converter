from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# API URL for real-time currency exchange rates
API_URL = "https://api.exchangerate-api.com/v4/latest/"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    amount = float(request.form['amount'])
    base_currency = request.form['base_currency']
    target_currencies = request.form.getlist('target_currencies')

    response = requests.get(API_URL + base_currency)
    data = response.json()

    if response.status_code != 200:
        return jsonify({'error': 'Failed to fetch exchange rates.'})

    conversions = {}
    for currency in target_currencies:
        rate = data['rates'].get(currency)
        if rate:
            conversions[currency] = round(amount * rate, 2)

    return jsonify(conversions)

if __name__ == '__main__':
    app.run(debug=True)
