import json
import socket
from socketserver import StreamRequestHandler, TCPServer

from message import Message

active_connections: list[socket.socket] = []

class EchoRequestHandler(StreamRequestHandler):
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

class TCP(TCPServer):
    def __init__(self, server_address, handler_class=EchoRequestHandler):
        self.allow_reuse_address = True
        super().__init__(server_address, handler_class)

    def send_all(self, data: bytearray) -> None:
        for connection in active_connections:
            try:
                connection.sendall(data)
            except Exception as e:
                print(f"Error sending message to TCP client: {e}")
