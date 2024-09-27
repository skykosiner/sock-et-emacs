import asyncio
import websocket
import dotenv

from command import Command
from flask import Flask
from get_data import get_data
from message import CommandType, Message
from system_command import SystemCommand
from tcp import TCP, EchoRequestHandler
from pyee.asyncio import AsyncIOEventEmitter

from utils import get_main_screen, start_in_thread
from vim import validate_vim_command

ee = AsyncIOEventEmitter()
main_screen = get_main_screen()

typeMessages = {
    "!vi": CommandType.vim_insert,
    "!va": CommandType.vim_after,
    "!vc": CommandType.vim_command,
    "asdf": CommandType.system_command,
    "!turn off screen": CommandType.system_command,
    "!change background": CommandType.system_command,
    "!i3 workspace": CommandType.system_command
}

system_commands = {
    # As my kinesis advantage 360 btw uses dvorak by deffalut and my system
    # needs to have qwerty for it to work, doing this will just mess up my
    # keyboard, won't turn it into qwerty though. Either way it's still more or
    # less imposible for me to type
    "asdf": SystemCommand("setxkbmap -layout real-prog-dvorak", "setxkbmap -layout us", 3, ee),
    "!turn off screen": SystemCommand(f"xrandr --output {main_screen} --brightness 0.05", f"xrandr --output {main_screen} --brightness 1", 5, ee),
    "!i3 workspace": SystemCommand("i3 workspace 69", "", 0, ee),
    "!change background": SystemCommand("change_background_random", "", 0, ee)
}

non_ws_sytem_commands = {
    "elvis": SystemCommand("/home/sky/.local/bin/elvis", "", 0, ee),
}

command = Command()

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

    command_handler(message)

async def main():
    dotenv.load_dotenv()

    current_loop = asyncio.get_event_loop()
    tcp = TCP(("localhost", 8080), EchoRequestHandler)
    start_in_thread(tcp.serve_forever)

    # ws = websocket.WebSocketApp("wss://skykosiner.com:8080", on_message=new_msg)
    ws = websocket.WebSocketApp("ws://127.0.0.1:42069", on_message=new_msg)
    start_in_thread(ws.run_forever)

    app = Flask(__name__)
    start_in_thread(lambda: app.run("127.0.0.1", 8081))

    @ee.on("emit-ws")
    def emit_ws(message: str) -> None:
        ws.send_text(message)

    @ee.on("vim")
    def vim_command(message: Message, tcp=tcp) -> None:
        message.message = message.message_without_command()
        valid = validate_vim_command(message)
        if not valid.is_good:
            ee.emit("emit-ws", valid.error)
            return

        buffer = command.reset().set_type(message.command).set_data(get_data(message)).buffer
        tcp.send_all(buffer)
        print(f"\033[32mSendning vim {message.command} with {message.message}\033[0m")

    @ee.on("system-command")
    def system_command(cmd: str, message: Message, tcp=tcp) -> None:
        buffer = command.reset().set_type(message.command).set_data(bytes(f"silent! !{cmd}", "ascii")).buffer
        tcp.send_all(buffer)
        print(f"\033[33mSending system command {cmd}.\033[0m")

    @ee.on("start-sys")
    def start_sys(message: Message) -> None:
        if message.command == CommandType.system_command:
            command = system_commands[message.message]
            if command:
                asyncio.ensure_future(command.add(message), loop=current_loop)

    # TODO: There must be a better way to define these routes then putting them all in the main function, it looks ugly
    @app.route("/elvis")
    def elvis():
        asyncio.ensure_future(non_ws_sytem_commands["elvis"].add(Message(CommandType.elvis, "")), loop=current_loop)
        return ""

    @app.route("/ceiling-lights-toggle")
    def ceiling_lights_toggle():
         return ""

    while True:
     await asyncio.sleep(1)  # Keep the event loop runnin:w

if __name__ == "__main__":
    asyncio.run(main())
