

import urllib.request
import json

def get_rates():
    url = "https://api.fixer.io/latest"
    req = urllib.request.Request(url, headers={'User-Agent': 'how code Currency Bot'})
    data = urllib.request.urlopen(req).read()
    data = json.loads(data.decode('utf-8'))
    rates = data["rates"]

    return rates

rates = get_rates()

def convert(amount, from_currency, to_currency):
    initial_amount = amount
    if from_currency != "EUR":
        amount = amount / rates[from_currency]
    if to_currency == "EUR":
        return initial_amount, from_currency, '=', amount, to_currency
    else:
        return initial_amount, from_currency, '=', amount * rates[to_currency], to_currency

print(rates)
print(convert(2.0,"EUR","USD"))
print(convert(1.0,"GBP","USD"))