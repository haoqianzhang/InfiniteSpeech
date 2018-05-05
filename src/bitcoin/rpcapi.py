import requests
from .core import Bitcoin


class BitcoinRPC(Bitcoin):
    url = 'http://13.94.56.21:8962'
    auth = ('rpcuser', '111111')
    headers = {'Content-Type': 'application/json'}
    jsonrpc = {'jsonrpc': '2.0', 'id': 'flask'}

    def create_request(self, json):
        return requests.post(self.url, headers=self.headers, auth=self.auth, json={**self.jsonrpc, **json})

    def get_blockchain_height(self):
        r = self.create_request({'method': 'getblockchaininfo'})
        return r.json()['result']['blocks']

    def get_block_hash(self, height):
        r = self.create_request({'method': 'getblockhash', 'params': [height]})
        return r.json()['result']

    def get_transactions_by_block_hash(self, hashcode):
        r = self.create_request({'method': 'getblock', 'params': [hashcode]})
        return r.json()['result']['tx']

    def get_transaction_by_hash(self, hashcode):
        r = self.create_request({'method': 'gettransaction', 'params': [hashcode]})
        return r.json()

    def get_raw_transaction_by_hash(self, hashcode):
        r = self.create_request({'method': 'getrawtransaction', 'params': [hashcode, True]})
        return r.json()
