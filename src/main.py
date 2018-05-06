from bitcoin import BitcoinRPC
from bitcoin import PostFactory
from flask import request
from flask_api import FlaskAPI

app = FlaskAPI('InfiniteSpeech')
rpc = BitcoinRPC()
factory = PostFactory(rpc)


@app.route('/posts/<int:count>', methods=['GET'])
@app.route('/posts/<int:count>/offset/<int:offset>')
def get_posts(count, offset=0):
    return [p.json for p in factory.get_posts(count, offset)]


@app.route('/quota', methods=['GET'])
def get_quota():
    unspent = rpc.list_unspent()[0]
    return {
        'quota': unspent['txid'],
        'vout': unspent['vout'],
        'amount': unspent['amount']
    }


@app.route('/post', methods=['POST'])
def send_post():
    return {'pid': rpc.send_raw_transaction(request.data['hex'])}
