import ByteStream from "bytestream.ts";
import "lz4ts";
import { siv } from "@noble/ciphers/aes";
import { randomBytes } from '@noble/ciphers/webcrypto';
import AskChecksumMessage from "./Protocol/AskChecksum";
import Storage from "./Storage";
import Message from "./Protocol/Message";
import ChecksumMessage from "./Protocol/Checksum";
import AskScriptMessage from "./Protocol/AskScript";
import ScriptMessage from "./Protocol/Script";
import { Socket } from "net";

export default class Client {
    storage: Storage;
    socket: Socket;
    key: Uint8Array;
    constructor(storage: Storage, socket: Socket, key: Uint8Array) {
        this.storage = storage;
        this.socket = socket;
        this.key = key;
    }

    finalize() {
        this.socket.destroy();
    }

    /** @internal */
    packAndSend(message: Message) {
        message.encode();
        const header = new ByteStream(1 + 4, "big", 0);

        let messageBytes = message.stream.byteArray;
        if (message.id == 53) {// script
            messageBytes = LZ4.compress(new Uint8Array(message.stream.byteArray));
            const originalSize = message.stream.byteArray.byteLength;
            const compressedSize = messageBytes.byteLength;
            console.log(`Compression ratio: ${Math.round((1-(compressedSize/originalSize))*100)}%`);
        }

        const nonce = randomBytes(12);
        messageBytes = siv(this.key, nonce)
            .encrypt(new Uint8Array(messageBytes));

        header.writeU8(message.id);
        header.writeBytes(nonce);
        header.writeU32(messageBytes.byteLength); // script can be big
        header.writeBytes(messageBytes);

        this.socket.write(new Uint8Array(header.byteArray));
    }

    unpackAndProcess(payload: Buffer) {
        const header = new ByteStream(payload.buffer, "big");
        const id = header.readU8();
        const nonce = header.readBytes(12);
        const size = header.readU16();
        const body = siv(this.key, new Uint8Array(nonce))
            .decrypt(new Uint8Array(header.readBytes(size)));

        switch (id) {
            case 50: {
                const message = new AskChecksumMessage(new ByteStream(body, "big"));
                message.decode();

                if (message.version != 2)
                    throw new Error("Invalid version!");

                const response = new ChecksumMessage();

                response.checksum = this.storage.checksum;
                this.packAndSend(response);
                break;
            }
            case 52: {
                const message = new AskScriptMessage(new ByteStream(body, "big"));
                message.decode();

                const response = new ScriptMessage();
                response.script = this.storage.script;
                this.packAndSend(response);
                break;
            }
            case 54: {
                this.finalize();
                return;
            }
        }
    }

    loop() {
        this.socket.on("data", (b) => this.unpackAndProcess(b));
        this.socket.on("error", (err) => console.warn(`Ignoring error ${err}`));
    }
}
