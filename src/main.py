import websocket
import threading

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

def vimCommannd(message: str) -> None:
    match message[0:3]:
        case "!vi" | "!va" | "!vc":
            ee.emit("vim", Message(command=typeMessages[message[0:3]], message=message))

def systemCommand(message: str) -> None:
    match message:
        case "asdf" | "!turn off screen" | "!change background" | "!i3 workspace":
            ee.emit("start-sys", Message(command=typeMessages[message], message=message))


def new_msg(_, message: str) -> None:
    print("Got message from websocket.", message)
    vimCommannd(message)

def main():
    tcp = TCP(("localhost", 8080), EchoRequestHandler)
    t = threading.Thread(target=tcp.serve_forever)
    t.daemon = True
    t.start()

    @ee.on("startc-sys")
    def handle_start_sys(msg: Message, tcp=tcp):
        syst

    ws = websocket.WebSocketApp("ws://localhost:42069", on_message=new_msg)
    ws.run_forever()

if __name__ == "__main__":
    main()

