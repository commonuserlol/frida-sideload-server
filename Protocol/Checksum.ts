import ByteStream from "bytestream.ts";
import Message from "./Message";

export default class ChecksumMessage extends Message {
    checksum: string;

    constructor(stream?: ByteStream) {
        super(stream);
        this.id = 51;
    }

    encode(): void {
        this.stream.writeU16(this.checksum.length);
        this.stream.writeBytes(new TextEncoder().encode(this.checksum));
    }
    
    decode(): void {}
}