import asyncio
import logging
from hashlib import sha256
from socket import socket
from time import time

from lz4.frame import compress, decompress

from Messages.Client.AskChecksum import AskChecksumMessage
from Messages.Client.AskScript import AskScriptMessage
from Messages.Message import Message
from Utils.ByteStream import ByteStream
from Utils.Storage import Storage


class Client:
    sock: socket
    storage: Storage

    def __init__(self, sock: socket, storage: Storage):
        self.sock = sock
        self.storage = storage

    def disconnect(self):
        self.sock.close()

    async def recv_data(self, max: int):
        loop = asyncio.get_event_loop()
        data = b''
        while True : # also add an interuption logic as break the loop if empty string or what you have there
            data += await loop.sock_recv(self.sock, 1)
            if data == b'' or len(data) == max:
                break

        return data

    async def recv_message(self) -> Message:
        loop = asyncio.get_event_loop()
        headerStream = ByteStream()
        headerStream.writeBytes(await loop.sock_recv(self.sock, 2 + 4 + 64))
        headerStream.offset = 0
        id = headerStream.readU16()
        size = headerStream.readU32()

        if size == 0:
            return

        checksum = headerStream.readBytes(64).decode("utf8")
        body = decompress(await self.recv_data(size))

        expectedChecksum = sha256(body).hexdigest()
        if expectedChecksum != checksum:
            raise RuntimeError("Data is corrupted")

        match id:
            case 1337:
                return AskChecksumMessage(self.storage)
            case 1339:
                return AskScriptMessage(self.storage)

    async def send_message(self, message: Message):
        message.encode()

        compressed = compress(message.stream.buffer, 16)
        checksum = sha256(message.stream.buffer).hexdigest()
        headerStream = ByteStream()
        headerStream.writeU16(message.id)
        headerStream.writeU32(len(compressed))
        headerStream.writeBytes(checksum.encode("utf8"))
        headerStream.writeBytes(compressed)

        loop = asyncio.get_event_loop()
        await loop.sock_sendall(self.sock, headerStream.buffer)

    async def loop(self):
        last_message_timestamp = int(time())
        while True:
            message = await self.recv_message()
            if message is None:
                if (last_message_timestamp + 5 >= int(time())):
                    await asyncio.sleep(0.5)
                    continue
                logging.info("Client disconnected")
                self.sock.close()
                return
            message.decode()
            message_to_send = message.process()

            if message_to_send:
                await self.send_message(message_to_send)
            last_message_timestamp = int(time())
