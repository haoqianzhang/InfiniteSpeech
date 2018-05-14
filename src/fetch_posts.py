from jsonschema import validate, ValidationError
from bitcoin import RawPostFactory, BitcoinRPC
from pymongo import MongoClient, errors
from datetime import datetime

MONGO_HOST = '127.0.0.1'
MONGO_PORT = 27017

schema = {
    'type': 'object',
    'required': [
        'name', 'email', 'title', 'content',
        'input_time', 'category', 'client', 'reply_to',
        'post_id', 'user_id',  # Now reliable
        'output_time',  # Need to be add by server when receive a transaction request
        # 'confirmed',  # Need to clear database first
    ],
    'properties': {
        'post_id': {'type': 'string'},
        'user_id': {'type': 'string'},
        'name': {'type': 'string'},
        'reply_to': {'type': 'string'},

        'title': {'type': 'string', 'maxLength': 100},
        'content': {'type': 'string'},

        'email': {
            'type': 'string',
            'maxLength': 100,
            'pattern': '(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)'
        },
        'category': {
            'type': 'string',
            'maxLength': 255,
            'pattern': '^(/[a-zA-Z0-9_.+-]+)+$'
        },
        'input_time': {'type': 'integer'},
        'output_time': {'type': 'integer'},
        'client': {'type': 'string', 'maxLength': 100},

        'confirmed': {'type': 'boolean'},
    },
}

if __name__ == '__main__':
    start_time = datetime.utcnow().timestamp()
    client = MongoClient(MONGO_HOST, MONGO_PORT)

    height_collection = client.test.height
    result = height_collection.find_one()
    if result is None:
        height_collection.insert_one({'height': 1})
        result = height_collection.find_one()

    height = int(result['height'])

    collection = client.test.posts
    factory = RawPostFactory(BitcoinRPC())
    count = 0
    for post in factory.get_posts(height):
        try:
            validate(post.json, schema)
        except ValidationError:
            continue

        try:
            collection.update_one({'post_id': post.id}, {'$set': post.json}, upsert=True)
            count += 1
        except errors.DuplicateKeyError:
            continue

    height_collection.update_one({'_id': result['_id']}, {'$set': {'height': factory.height + 1}})

    end_time = datetime.utcnow().timestamp()

    print(
        "Insert {} post(s), search post from height {} to {}, {:.3f} seconds"
        .format(count, height, factory.height + 1, end_time - start_time)
    )
