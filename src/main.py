from bitcoin import BitcoinRPC
from post import get_posts as posts
from flask import request
from flask_api import FlaskAPI
from codecs import decode
import json
from fetch_posts import schema, MONGO_PORT, MONGO_HOST
from pymongo import MongoClient
from jsonschema import validate, ValidationError
from datetime import datetime

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
    hexstring = request.data['hex']
    transaction = rpc.decode_raw_transaction(hexstring)
    raw_content = transaction['vout'][0]['scriptPubKey']['asm']

    if 'OP_RETURN' not in raw_content:
        return {'error': 'Transaction does not contain real content.'}
    hex_str = raw_content.lstrip('OP_RETURN ')
    content = decode(hex_str, 'hex').decode('utf-8')
    json_content = json.loads(content)
    json_content['post_id'] = transaction['txid']
    json_content['user_id'] = transaction['vout'][1]['scriptPubKey']['addresses'][0]
    json_content['input_time'] = int(datetime.utcnow().timestamp())
    json_content['output_time'] = int(datetime.utcnow().timestamp())
    json_content['confirmed'] = False

    try:
        validate(json_content, schema)
    except ValidationError as e:
        return {'error': 'JSON validation failed. ' + e.message}

    client = MongoClient(MONGO_HOST, MONGO_PORT)
    collection = client.test.posts
    collection.insert_one(json_content)

    return {'pid': rpc.send_raw_transaction(hexstring)}
