from .interfaces import Bitcoin
from codecs import decode
import json


class RawPost:
    def __init__(self, rpc_instance: Bitcoin, transaction_id: str, height: int):
        self.rpc = rpc_instance
        self.id = transaction_id
        self.author = self.__get_author()
        self.time = 0
        self.raw_content = self.__get_raw_content()
        self.content = self.__get_content()
        self.confirmations = 0
        self.json = self.__get_json()
        self.json['post_id'] = self.id
        self.json['user_id'] = self.author
        self.json['output_time'] = self.time
        self.json['confirmed'] = True
        self.json['height'] = height

    def __get_raw_content(self):
        t = self.rpc.get_raw_transaction_by_hash(self.id)
        self.time = t['result']['time']
        return t['result']['vout'][0]['scriptPubKey']['asm']

    def __get_author(self):
        t = self.rpc.get_transaction_by_hash(self.id)
        return t['result']['details'][1]['address']

    def __get_content(self):
        if 'OP_RETURN' not in self.raw_content:
            raise self.Error('Transaction does not contain real content.')
        hex_str = self.raw_content.lstrip('OP_RETURN ')
        return decode(hex_str, 'hex').decode('utf-8')

    def __get_json(self):
        return json.loads(self.content)

    class Error(Exception):
        pass


class RawPostFactory:

    def __init__(self, rpc_instance: Bitcoin):
        self.rpc = rpc_instance
        self.height = 1

    def get_posts(self, height=1) -> list:
        """
        通过查找指定数量的 block 的内容生成 Post 类，如果数据内容不能正确解析则跳过

        TODO: 实现 Post 偏移量而不是 Block 的偏移量

        :param height:
        :return: 可以成功解析的 Post
        """
        self.height = self.rpc.get_blockchain_height()
        if height < 1 or height > self.height:
            return []

        posts = []
        position = height
        while position <= self.height:
            position += 1

            try:
                hashcode = self.rpc.get_block_hash(position - 1)
                tids = self.rpc.get_transactions_by_block_hash(hashcode)
            except TypeError:
                continue

            if len(tids) < 2:
                continue

            for tid in tids:
                try:
                    p = RawPost(self.rpc, tid, position)
                    p.confirmations = self.height - position + 1
                    posts.append(p)
                except (IndexError, TypeError, RawPost.Error, json.JSONDecodeError):
                    continue

        return posts
