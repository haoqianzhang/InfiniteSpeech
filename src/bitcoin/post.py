from .core import Bitcoin
from codecs import decode
import json


class Post:
    def __init__(self, rpc_instance: Bitcoin, transaction_id):
        self.rpc = rpc_instance
        self.id = transaction_id
        self.author = self.__get_author()
        self.raw_content = self.__get_raw_content()
        self.content = self.__get_content()
        self.json = self.__get_json()

    def __get_raw_content(self):
        t = self.rpc.get_raw_transaction_by_hash(self.id)
        return t['result']['vout'][0]['scriptPubKey']['asm']

    def __get_author(self):
        t = self.rpc.get_transaction_by_hash(self.id)
        return t['result']['details'][1]['address']

    def __get_content(self):
        if 'OP_RETURN' not in self.raw_content:
            raise self.Error('Transaction did not contains real content.')
        hex_str = self.raw_content.lstrip('OP_RETURN ')
        return decode(hex_str, 'hex').decode('utf-8')

    def __get_json(self):
        return json.loads(self.content)

    class Error(Exception):
        pass


class PostFactory:

    def __init__(self, rpc_instance: Bitcoin):
        self.rpc = rpc_instance

    def get_post(self, count, offset=0):
        """
        通过查找指定数量的 block 的内容生成 Post 类，如果数据内容不能正确解析则跳过

        :param count: Block 的数量
        :param offset: Height 偏移量
        :return: 可以成功解析的 Post
        """
        height = self.rpc.get_blockchain_height()
        hashcodes = [self.rpc.get_block_hash(i) for i in range(height - count - offset + 1, height - offset + 1)]

        tids = []
        for code in hashcodes:
            t = self.rpc.get_transactions_by_block_hash(code)
            if len(t) > 1:
                tids = [*tids, *t]

        posts = []
        for tid in tids:
            try:
                p = Post(self.rpc, tid)
                posts.append(p)
            except (IndexError, Post.Error, json.JSONDecodeError):
                continue

        return posts
