import websocket
import json
import threading

from message import Command, Message
from tcp import TCP, EchoRequestHandler
from pyee.base import EventEmitter

ee = EventEmitter()

def new_msg(ws: websocket.WebSocket, message: str):
    json_object = json.loads(message)
    msg = Message(**json_object)
    print(f"WebSocket message: {msg}")

    ee.emit("ws-msg", msg)



def main():
    tcp = TCP(("localhost", 8080), EchoRequestHandler)
    t = threading.Thread(target=tcp.serve_forever)
    t.daemon = True
    t.start()

    @ee.on("ws-msg")
    def handle_ws_msg(msg: Message, tcp=tcp):
        tcp.send_all(msg)

    ws = websocket.WebSocketApp("ws://localhost:42069", on_message=new_msg)
    ws.run_forever()

if __name__ == "__main__":
    main()

