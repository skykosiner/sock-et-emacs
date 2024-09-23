import { WS } from "./ws.js";
const ws = new WS("ws://127.0.0.1:42069");
setTimeout(() => {
    ws.send("!vi test");
}, 1000);
