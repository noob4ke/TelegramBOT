import requests
import json


url = "https://www.cbr-xml-daily.ru/daily_json.js"
url_btc = "https://blockchain.info/ru/ticker"


def btc_usd():
    j = requests.get(url_btc)
    data = json.loads(j.text)
    btc = data["USD"]["last"]
    return f"Курс BTC сейчас {btc}$"


def check(value):
    data = json.loads(requests.get(url).text)
    price = data["Valute"][value]['Value']
    return f"Курс {value} сейчас {round(price, 2)}₽"
