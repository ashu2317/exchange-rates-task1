from flask import Flask, jsonify
import requests
import json

app = Flask(__name__)


@app.route("/api/v1/<string:from_currency>/<string:to_currency>/<string:amount>", methods=["GET"])
def get_me_exchange_value(from_currency, to_currency, amount):
    data = json.loads(requests.get(construct_url(from_currency, to_currency)).text)
    key = from_currency + '_' + to_currency
    current_rate = (data[key])['val']

    return jsonify(response_generator(from_currency, to_currency, amount, current_rate)), 200


def response_generator(from_currency, to_currency, from_amount, exchange_rate):
    return {
        "from_currency": from_currency,
        "to_currency": to_currency,
        "from_amount": from_amount,
        "to_amount": float(from_amount) * float(exchange_rate),
        "exchange_rate": exchange_rate
    }


def construct_url(from_currency, to_currency):
    return 'https://free.currencyconverterapi.com/api/v6/convert?q=%s_%s&compact=y' % (from_currency, to_currency)


if __name__ == '__main__':
    app.run(debug=False)
