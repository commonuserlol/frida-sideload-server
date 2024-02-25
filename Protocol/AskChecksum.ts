import ByteStream from "bytestream.ts";
import Message from "./Message";

export default class AskChecksumMessage extends Message {
    version: number;

    constructor(stream?: ByteStream) {
        super(stream);
        this.id = 50;
    }
    encode(): void {}
    
    decode(): void {
        this.version = this.stream.readU8();
    }
}