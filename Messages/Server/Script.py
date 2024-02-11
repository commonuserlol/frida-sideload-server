from Messages.Message import Message

class ScriptMessage(Message):
    def __init__(self, *args):
        super().__init__(*args)
        self.id = 1340

    def decode(self):
        pass

    def encode(self):
        self.stream.writeU32(len(self.storage.script))
        self.stream.writeBytes(self.storage.script)

    def process(self):
        pass

    def is_client_to_server(self):
        return False
