from Messages.Message import Message

class ChecksumMessage(Message):
    def __init__(self, *args):
        super().__init__(*args)
        self.id = 1338

    def decode(self):
        pass

    def encode(self):
        checksum = self.storage.checksum.encode("utf8")
        self.stream.writeU8(len(checksum))
        self.stream.writeBytes(checksum)

    def process(self):
        pass

    def is_client_to_server(self):
        return False
