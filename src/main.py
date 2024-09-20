import websocket
import threading
import time

from message import Command, Message
from system_command import SystemCommand
from tcp import TCP, EchoRequestHandler
from pyee.base import EventEmitter

from utils import get_main_screen

ee = EventEmitter()
main_screen = get_main_screen()

typeMessages = {
    "!vi": Command.vim_insert,
    "!va": Command.vim_after,
    "!vc": Command.vim_command,
    "asdf": Command.system_command,
    "!turn off screen": Command.system_command,
    "!change background": Command.system_command,
    "!i3 workspace": Command.system_command
}

system_commands = {
    # As my kinesis advantage 360 btw uses dvorak by deffalut and my system
    # needs to have qwerty for it to work, doing this will just mess up my
    # keyboard, won't turn it into qwerty though. Either way it's still more or
    # less imposible for me to type
    "asdf": SystemCommand("setxbmap -layout real-prog-dvorak", "setxbmap -layout us", 3000, ee),
    "!turn off screen": SystemCommand(f"xrandr --output {main_screen} --brightness 0.05", f"xrandr --output {main_screen} --brightness 1", 5000, ee),
    "!i3 worskpace": SystemCommand("i3 workspace 69", "", 0, ee),
    "!change background": SystemCommand("change_background_random", "", 0, ee)
}

def start_in_thread(target, daemon=True):
    """Helper to start any target function in a daemon thread."""
    thread = threading.Thread(target=target)
    thread.daemon = daemon
    thread.start()
    return thread

def command_handler(message: str) -> None:
    command_prefix = message[:3]

    if command_prefix in typeMessages:
        command = typeMessages[command_prefix]
        ee.emit("vim", Message(command=command, message=message))
    elif message in typeMessages:
        command = typeMessages[message]
        ee.emit("start-sys", Message(command=command, message=message))


def new_msg(_, message: str) -> None:
    if len(message) < 3:
        ee.emit("emit-ws", "It's so over, your message isn't longer then 3 chars.")
        return

    print("Got message from websocket.", message)
    command_handler(message)

def main():
    tcp = TCP(("localhost", 8080), EchoRequestHandler)
    start_in_thread(tcp.serve_forever)

    ws = websocket.WebSocketApp("ws://localhost:42069", on_message=new_msg)
    start_in_thread(ws.run_forever)

    @ee.on("emit-ws")
    def emit_ws(message: str) -> None:
        ws.send_text(message)

    @ee.on("start-sys")
    def start_sys(message: Message) -> None:
        print(message)

   # Keep the main thread alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down...")


if __name__ == "__main__":
    main()

