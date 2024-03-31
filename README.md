**USE FRIDA PORTAL INSTEAD**<br>

# frida-sideload-server
Server-side part for [frida-sideload](https://github.com/commonuserlol/frida-sideload-client)

# Usage
0. Install nodejs
1. Clone this repo
2. **CHANGE ENCRYTION KEY inside index.ts**
3. Compile with `npx esbuild --bundle index.ts --outfile=index.cjs --platform=node`
4. Change your remote script inside `target.js`
5. Run with `node index.cjs`

# License
This project is licensed under two licenses:
* **GNU AGPLv3 only** for the client (this is a module, you can use it for commercial purposes if you do not change the module code)
* **MIT** for the server (this is not a module)
