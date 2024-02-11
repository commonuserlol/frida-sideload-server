from Messages.Message import Message
from Messages.Server.Checksum import ChecksumMessage


class AskChecksumMessage(Message):
    def __init__(self, *args):
        super().__init__(*args)
        self.id = 1337

    def decode(self):
        pass

    def encode(self):
        pass

    def process(self):
        return ChecksumMessage(self.storage)

    def is_client_to_server(self):
        return True
