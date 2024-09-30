import os
import dotenv
import asyncio
import websocket

from flask import Flask
from flask_cors import CORS
from setup_routes import setup_routes
from homeassitant import HomeAssistant
from tcp import TCP, EchoRequestHandler
from system_command import SystemCommand
from message import CommandType, Message
from pyee.asyncio import AsyncIOEventEmitter
from setup_listen_events import setup_listen_events
from utils import get_main_screen, start_in_thread

ee = AsyncIOEventEmitter()
main_screen = get_main_screen()

typeMessages = {
    "!vi": CommandType.vim_insert,
    "!va": CommandType.vim_after,
    "!vc": CommandType.vim_command,
    "asdf": CommandType.system_command,
    "!turn off screen": CommandType.system_command,
    "!change background": CommandType.system_command,
    "!i3 workspace": CommandType.system_command,
}

system_commands = {
    # As my kinesis advantage 360 btw uses dvorak by deffalut and my system
    # needs to have qwerty for it to work, doing this will just mess up my
    # keyboard, won't turn it into qwerty though. Either way it's still more or
    # less imposible for me to type
    "asdf": SystemCommand(
        "setxkbmap -layout real-prog-dvorak", "setxkbmap -layout us", 3, ee
    ),
    "!turn off screen": SystemCommand(
        f"xrandr --output {main_screen} --brightness 0.05",
        f"xrandr --output {main_screen} --brightness 1",
        5,
        ee,
    ),
    "!i3 workspace": SystemCommand("i3 workspace 69", "", 0, ee),
    "!change background": SystemCommand("change_background_random", "", 0, ee),
}


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
    url, token = os.getenv("HOME_ASSISTANT_URL"), os.getenv("HOME_ASSISTANT_TOKEN")

    if not url or not token:
        print("Url and or token not found, it's joever")
        exit(0x45)

    current_loop = asyncio.get_event_loop()
    tcp = TCP(("localhost", 8080), EchoRequestHandler)
    start_in_thread(tcp.serve_forever)

    home_assistant = HomeAssistant(url, token, tcp)

    # ws = websocket.WebSocketApp("wss://skykosiner.com:8080", on_message=new_msg)
    ws = websocket.WebSocketApp("ws://127.0.0.1:42069", on_message=new_msg)
    start_in_thread(ws.run_forever)

    app = Flask(__name__)
    start_in_thread(lambda: app.run("127.0.0.1", 8081))

    CORS(app, origins="*")

    setup_listen_events(ee, ws, tcp, system_commands, current_loop)
    setup_routes(app, current_loop, ee, home_assistant)

    while True:
        await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(main())
