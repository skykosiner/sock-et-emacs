import socketserver
import websocket
import json
import threading
from dataclasses import dataclass
from enum import Enum

class Command(Enum):
    vim_insert = 0
    vim_normal = 1
    system_command = 2

@dataclass
class Message:
    command: Command
    message: str

active_connections = []

class EchoHandler(socketserver.StreamRequestHandler):
    def handle(self):
        active_connections.append(self.request)

        try:
            self.request.sendall("Welecome in. We're so back".encode())

            while True:
                msg = self.request.recv(1024).decode()
                if not msg:
                    break
                print(f"Received from TCP: {msg}")
                self.request.sendall(msg.encode())
        finally:
            # Remove the connection when done
            active_connections.remove(self.request)

def new_msg(ws: websocket.WebSocket, message: str):
    json_object = json.loads(message)
    msg = Message(**json_object)
    print(f"WebSocket message: {msg}")

    if msg.command != Command.system_command and len(msg.message) > 5:
        print("???")
        ws.send("Message can't be greater then 5 chars")
        return

    # Broadcast the WebSocket message to all active TCP connections
    broadcast_to_tcp_clients(msg.message)

def broadcast_to_tcp_clients(message: str):
    for connection in active_connections:
        try:
            connection.sendall(message.encode())
        except Exception as e:
            print(f"Error sending message to TCP client: {e}")

def start_tcp_server():
    server = socketserver.TCPServer(("", 8080), EchoHandler)
    print("TCP server started on port 8080")
    server.serve_forever()

def start_websocket_client():
    ws = websocket.WebSocketApp("ws://localhost:42069", on_message=new_msg)
    print("WebSocket client connected to ws://localhost:42069")
    ws.run_forever()

def main():
    tcp_thread = threading.Thread(target=start_tcp_server, daemon=True)
    tcp_thread.start()

    start_websocket_client()

if __name__ == "__main__":
    main()

