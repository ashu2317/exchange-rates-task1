from flask import Flask, jsonify
import requests
import json
from endpoint.exchange_dictionary import ExchangeDictionary
import os

app = Flask(__name__)
port = int(os.getenv("VCAP_APP_PORT"))
# clear Map in every one hour
ExchangeDictionary.clear_exchange_rate_map_in_every_hour()


@app.route("/api/v1/<string:from_currency>/<string:to_currency>/<string:amount>", methods=["GET"])
def get_me_exchange_value(from_currency, to_currency, amount):
    key = from_currency + '_' + to_currency
    if ExchangeDictionary.exchange_rate_map.get(key) is None:
        data = json.loads(requests.get(construct_url(from_currency, to_currency)).text)
        current_rate = (data[key])['val']
        ExchangeDictionary.exchange_rate_map[key] = current_rate

    return jsonify(
        response_generator(from_currency, to_currency, amount, ExchangeDictionary.exchange_rate_map.get(key))), 200


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
    app.run(host="0.0.0.0", port=port)
