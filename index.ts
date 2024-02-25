import { Socket, createServer } from "net";
import Client from "./Client";
import Storage from "./Storage";

const storage = new Storage("./target.js");
storage.load();
const KEY = new Uint8Array(
    [109, 121, 115, 117, 112, 101, 114, 115, 101, 99, 114, 101, 116, 107, 101, 121, 109, 121, 115, 117, 112, 101, 114, 115, 101, 99, 114, 101, 116, 107, 101, 121]
);

function listener(socket: Socket) {
    const client = new Client(storage, socket, KEY);
    client.loop();
}

const server = createServer(listener);
server.listen(1337, "0.0.0.0");
console.log("Server ready!");
