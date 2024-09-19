import { WebSocket, WebSocketServer } from "ws";

enum Command {
    vimInsert,
    vimNormal,
    systemCommand
}

type Message = {
    command: Command,
    message: string,
}

const test: string = "";

test.split("").map((char) => {
    if (char !== "." || !isNaN(parseInt(char))) {
        console.log(char);
    }
});

function getCommandType(msg: string): Command | null {
    switch (msg.substring(0, 3)) {
        case "!vi":
            return Command.vimInsert
        case "!vn":
            return Command.vimNormal
        case "!sc":
            return Command.systemCommand
        default:
            return null
    }
}

const connections: Array<WebSocket> = [];

const ws = new WebSocketServer({ port: 42069 });
ws.on("error", (err) => {
    console.error("It's so over", err);
});

ws.on("connection", (socketItToMeBBG) => {
    connections.push(socketItToMeBBG);

    socketItToMeBBG.on("message", (message) => {
        connections.map(con => {
            const commandType = getCommandType(message.toString());

            if (commandType === null) {
                socketItToMeBBG.send("Invalid command type.");
                return;
            }

            const msg: Message = {
                message: message.toString().substring(3),
                command: commandType,
            }


            if (con != socketItToMeBBG) {
                con.send(JSON.stringify(msg));
            }
        })
    });
});
