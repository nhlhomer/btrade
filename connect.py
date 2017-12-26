# GDAX testing

import os, json, hmac, hashlib, time, requests, base64
from requests.auth import AuthBase

# Create custom authentication for Exchange
class CoinbaseExchangeAuth(AuthBase):
    def __init__(self, api_key, secret_key, passphrase):
        self.api_key = api_key
        self.secret_key = secret_key
        self.passphrase = passphrase

    def __call__(self, request):
        timestamp = str(time.time())
        message = timestamp + request.method + request.path_url + (request.body or '')
        hmac_key = base64.b64decode(self.secret_key)
        signature = hmac.new(hmac_key, message, hashlib.sha256)
        signature_b64 = signature.digest().encode('base64').rstrip('\n')

        request.headers.update({
            'CB-ACCESS-SIGN': signature_b64,
            'CB-ACCESS-TIMESTAMP': timestamp,
            'CB-ACCESS-KEY': self.api_key,
            'CB-ACCESS-PASSPHRASE': self.passphrase,
            'Content-Type': 'application/json'
        })
        return request

with open("/Users/Minnie/Marc-Code/marc-git/secrets.json") as f:
    secrets = json.loads(f.read())

api_url = 'https://api.gdax.com/'
auth = CoinbaseExchangeAuth(secrets[GDAX_API_KEY], secrets[GDAX_SECRET], secrets[GDAX_PASSPHRASE])

# Get accounts
r = requests.get(api_url + 'accounts', auth=auth)
print r.json()
# [{"id": "a1b2c3d4", "balance":...

# Place an order
# order = {
#    'size': 1.0,
#    'price': 1.0,
#    'side': 'buy',
#    'product_id': 'BTC-USD',
#}
#r = requests.post(api_url + 'orders', json=order, auth=auth)
#print r.json()
# {"id": "0428b97b-bec1-429e-a94c-59992926778d"}

