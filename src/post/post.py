from pymongo import MongoClient, DESCENDING

MONGO_HOST = '127.0.0.1'
MONGO_PORT = 27017


def get_posts(count: int, offset: int, height: int) -> list:
    client = MongoClient(MONGO_HOST, MONGO_PORT)
    collection = client.test.posts
    posts = []
    for post in collection.find(limit=count, skip=offset).sort('output_time', DESCENDING):
        post.pop('_id', None)
        if post['confirmed']:
            post['confirmations'] = height - post['height'] + 1
        else:
            post['confirmations'] = 0
        posts.append(post)
    client.close()
    return posts
