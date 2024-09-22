import { WebSocket, WebSocketServer } from "ws";

const connections: Array<WebSocket> = [];

const ws = new WebSocketServer({ port: 42069 });
ws.on("error", (err) => {
    console.error("It's so over", err);
});

ws.on("connection", (socketItToMeBBG) => {
    connections.push(socketItToMeBBG);
    socketItToMeBBG.on("message", (message) => {
        connections.map(con => {
            if (con != socketItToMeBBG) {
                con.send(message.toString());
            }
        })
    });
});
