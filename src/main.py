from bitcoin import BitcoinRPC
from bitcoin import PostFactory

from pprint import PrettyPrinter

p = PrettyPrinter(indent=2)

factory = PostFactory(BitcoinRPC())
p.pprint([post.json for post in factory.get_post(10, 32)])
