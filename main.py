from socket import socket, SOL_SOCKET, SO_REUSEADDR, SO_REUSEPORT
import logging
import asyncio

from Utils.Storage import Storage
from Client import Client


logging.basicConfig(level=logging.DEBUG)

class Server:
    sock: socket
    storage: Storage

    def __init__(self, port: int, config_path = "index.js"):
        self.server = socket()
        self.storage = Storage(config_path)
        self.server.bind(("", port))
        self.server.listen(8)
        self.server.setblocking(False)
        self.server.setsockopt(SOL_SOCKET, SO_REUSEADDR | SO_REUSEPORT, 1)

    async def listen(self):
        loop = asyncio.get_event_loop()

        while True:
            try:
                client, addr = await loop.sock_accept(self.server)
                logging.info(f"Client ({addr[0]}) accepted")
                instance = Client(client, self.storage)
                loop.create_task(instance.loop())
            except KeyboardInterrupt:
                break

server = Server(1337)
asyncio.run(server.listen())
