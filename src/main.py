from bitcoin import BitcoinRPC
from post import get_posts as posts
from flask import request
from flask_api import FlaskAPI

app = FlaskAPI('InfiniteSpeech')
rpc = BitcoinRPC()


@app.route('/posts/<int:count>', methods=['GET'])
@app.route('/posts/<int:count>/offset/<int:offset>')
def get_posts(count, offset=0):
    return posts(count, offset)


@app.route('/quota', methods=['GET'])
def get_quota():
    unspent = rpc.list_unspent()[0]
    return {
        'txid': unspent['txid'],
        'vout': unspent['vout'],
        'amount': unspent['amount']
    }


@app.route('/post', methods=['POST'])
def send_post():
    return {'pid': rpc.send_raw_transaction(request.data['hex'])}
