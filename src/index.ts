import { WS } from "./ws.js";

const ws = new WS("ws://127.0.0.1:42069");
const newMessageForm = document.getElementById("newMessageForm");

newMessageForm.addEventListener("submit", (e) => {
    e.preventDefault();

    //@ts-ignore
    const newMessage: string = document.getElementById("newMessage").value;

    if (newMessage.trim() !== "") {
        ws.send(newMessage);
    }
})
