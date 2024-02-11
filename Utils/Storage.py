from hashlib import sha256


class Storage:
    def __init__(self, script_path: str):
        with open(script_path, "rb") as f:
            self.script = f.read()
        self.checksum = sha256(self.script).hexdigest()
