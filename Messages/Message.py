from abc import abstractmethod
from Utils.ByteStream import ByteStream
from Utils.Storage import Storage


class Message:
    stream: ByteStream
    storage: Storage

    id: int

    def __init__(self, storage: Storage, stream: ByteStream | None = None):
        self.stream = ByteStream() if stream is None else stream
        self.storage = storage

    @abstractmethod
    def decode(self):
        pass

    @abstractmethod
    def encode(self):
        pass

    @abstractmethod
    def process(self):
        pass

    @abstractmethod
    def is_client_to_server(self) -> bool:
        pass
