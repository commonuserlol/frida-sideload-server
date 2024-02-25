import ByteStream from "bytestream.ts";
import Message from "./Message";

export default class ScriptMessage extends Message {
    script: string;

    constructor(stream?: ByteStream) {
        super(stream);
        this.id = 53;
    }

    encode(): void {
        this.stream.writeU32(this.script.length);
        this.stream.writeBytes(new TextEncoder().encode(this.script));
    }
    
    decode(): void {}
}