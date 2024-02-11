class ByteStream:
    def __init__(self, buffer=b''):
        self.buffer = bytearray(buffer)
        self.offset = 0

    def readBytes(self, length: int):
        array = self.buffer[self.offset:self.offset+length]
        self.offset += length
        return array

    def readU8(self):
        return int.from_bytes(self.readBytes(1), "big", signed=False)

    def readS8(self):
        return int.from_bytes(self.readBytes(1), "big", signed=True)

    def readU16(self):
        return int.from_bytes(self.readBytes(2), "big", signed=False)

    def readS16(self):
        return int.from_bytes(self.readBytes(2), "big", signed=True)

    def readU32(self):
        return int.from_bytes(self.readBytes(4), "big", signed=False)

    def readS32(self):
        return int.from_bytes(self.readBytes(4), "big", signed=True)

    def writeBytes(self, array):
        self.buffer += array
        self.offset += len(array)

    def writeU8(self, value:int):
        self.writeBytes(int.to_bytes(value, 1, "big", signed=False))

    def writeS8(self, value:int):
        self.writeBytes(int.to_bytes(value, 1, "big", signed=True))

    def writeU16(self, value:int):
        self.writeBytes(int.to_bytes(value, 2, "big", signed=False))

    def writeS16(self, value:int):
        self.writeBytes(int.to_bytes(value, 2, "big", signed=True))

    def writeU32(self, value:int):
        self.writeBytes(int.to_bytes(value, 4, "big", signed=False))

    def writeS32(self, value:int):
        self.writeBytes(int.to_bytes(value, 4, "big", signed=True))
