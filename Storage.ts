import { createHash } from "crypto";
import { readFileSync } from "fs";

export default class Storage {
    path: string;
    script: string;
    checksum: string;

    constructor(path: string) {
        this.path = path;
        this.script = "";
        this.checksum = "";
    }

    load() {
        const bytes = readFileSync(this.path);
        this.script = new TextDecoder().decode(bytes);
        const hash = createHash("sha512");
        hash.update(bytes);
        this.checksum = hash.digest("hex");
    }
}