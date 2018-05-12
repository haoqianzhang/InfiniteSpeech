from pymongo import MongoClient, DESCENDING

MONGO_HOST = '127.0.0.1'
MONGO_PORT = 27017


def get_posts(count: int, offset: int) -> list:
    client = MongoClient(MONGO_HOST, MONGO_PORT)
    collection = client.test.posts
    posts = []
    for post in collection.find(limit=count, skip=offset).sort('output_time', DESCENDING):
        post.pop('_id', None)
        posts.append(post)
    client.close()
    return posts
