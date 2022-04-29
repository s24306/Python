import requests
import json

have = input()
currency_need = input()
amount = float(input())
rates = {}
usd = requests.get("http://www.floatrates.com/daily/usd.json")
usd = json.loads(usd.text)
rates['usd'] = usd
eur = requests.get("http://www.floatrates.com/daily/eur.json")
eur = json.loads(eur.text)
rates['eur'] = eur

ex_rate = ["usd", "eur"]
while True:
    print('Checking the cache…')
    if currency_need in ex_rate:
        print("Oh! It is in the cache!")
        received = round(float(amount) * rates[currency_need][have]['inverseRate'], 2)
        print(f"You received {received} {currency_need}.")
    else:
        print("Sorry, but it is not in the cache!")
        ex_rate.append(currency_need)
        r = requests.get("http://www.floatrates.com/daily/{}.json".format(currency_need))
        r = json.loads(r.text)
        rates[currency_need] = r
        received = round(float(amount) * r[have]['inverseRate'], 2)
        print(f"You received {received} {currency_need}.")
    currency_need = input()
    if currency_need == "":
        break
    amount = input()
    if amount == "":
        break
