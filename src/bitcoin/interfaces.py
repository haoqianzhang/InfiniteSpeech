from abc import abstractmethod, ABCMeta


class Bitcoin(metaclass=ABCMeta):
    @abstractmethod
    def get_blockchain_height(self) -> int:
        pass

    @abstractmethod
    def get_block_hash(self, height: int) -> str:
        pass

    @abstractmethod
    def get_transactions_by_block_hash(self, hashcode: str) -> list:
        pass

    @abstractmethod
    def get_transaction_by_hash(self, hashcode: str) -> dict:
        pass

    @abstractmethod
    def get_raw_transaction_by_hash(self, hashcode: str) -> dict:
        pass

    @abstractmethod
    def list_unspent(self):
        pass

    @abstractmethod
    def send_raw_transaction(self, hexstring: str) -> str:
        pass

    @abstractmethod
    def decode_raw_transaction(self, hexstring: str) -> str:
        pass
