import asyncio
import os
import websocket
import dotenv
import random

from vim_colorscheme import VimColorScheme
from homeassitant import HomeAssistant
from command import Command
from flask import Flask, jsonify
from flask_cors import CORS
from get_data import get_data
from message import CommandType, Message
from system_command import SystemCommand
from tcp import TCP, EchoRequestHandler
from pyee.asyncio import AsyncIOEventEmitter

from utils import get_main_screen, start_in_thread
from vim import validate_vim_command

ee = AsyncIOEventEmitter()
main_screen = get_main_screen()
command = Command()

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

non_ws_sytem_commands = {
    "elvis": SystemCommand("/home/sky/.local/bin/elvis", "", 0, ee),
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

    home_assistant = HomeAssistant(url, token)

    current_loop = asyncio.get_event_loop()
    tcp = TCP(("localhost", 8080), EchoRequestHandler)
    start_in_thread(tcp.serve_forever)

    # ws = websocket.WebSocketApp("wss://skykosiner.com:8080", on_message=new_msg)
    ws = websocket.WebSocketApp("ws://127.0.0.1:42069", on_message=new_msg)
    start_in_thread(ws.run_forever)

    app = Flask(__name__)
    start_in_thread(lambda: app.run("127.0.0.1", 8081))

    CORS(app, origins="*")

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

        buffer = (
            command.reset().set_type(message.command).set_data(get_data(message)).buffer
        )
        tcp.send_all(buffer)
        print(f"\033[32mSendning vim {message.command} with {message.message}\033[0m")

    @ee.on("system-command")
    def system_command(cmd: str, message: Message, tcp=tcp) -> None:
        buffer = (
            command.reset()
            .set_type(message.command)
            .set_data(bytes(f"silent! !{cmd}", "ascii"))
            .buffer
        )
        tcp.send_all(buffer)
        print(f"\033[33mSending system command {cmd}.\033[0m")

    @ee.on("start-sys")
    def start_sys(message: Message) -> None:
        if message.command == CommandType.system_command:
            command = system_commands[message.message]
            if command:
                asyncio.ensure_future(command.add(message), loop=current_loop)

    @ee.on("vim-color")
    def vim_color(color: str) -> None:
        print(f"\033[32mChanging vim colorscheme too {color}\033[0m")
        buffer = (
            command.reset()
            .set_type(CommandType.vim_colors)
            .set_data(bytes(f"silent colorscheme {color}", "ascii"))
            .buffer
        )
        tcp.send_all(buffer)

    # TODO: There must be a better way to define these routes then putting them all in the main function, it looks ugly
    @app.route("/api/change_vim_color")
    def change_vim_color():
        colorschemes = [
            "ayu",
            "ayu-dark",
            "ayu-light",
            "ayu-mirage",
            "blue",
            "carbonfox",
            "catppuccin",
            "catppuccin-frappe",
            "catppuccin-latte",
            "catppuccin-macchiato",
            "catppuccin-mocha",
            "colorbuddy",
            "darkblue",
            "dawnfox",
            "dayfox",
            "default",
            "delek",
            "desert",
            "duskfox",
            "elflord",
            "evening",
            "gruvbox",
            "gruvbox-material",
            "gruvbuddy",
            "habamax",
            "industry",
            "koehler",
            "lunaperche",
            "morning",
            "murphy",
            "nightfox",
            "nordfox",
            "onedark",
            "pablo",
            "peachpuff",
            "quiet",
            "retrobox",
            "ron",
            "rose-pine",
            "rose-pine-dawn",
            "rose-pine-main",
            "rose-pine-moon",
            "shine",
            "slate",
            "sorbet",
            "terafox",
            "tokyonight",
            "tokyonight-day",
            "tokyonight-moon",
            "tokyonight-night",
            "tokyonight-storm",
            "torte",
            "vim",
            "wildcharm",
            "zaibatsu",
            "zellner",
        ]

        random_color_scheme = random.choice(colorschemes)
        asyncio.ensure_future(VimColorScheme(random_color_scheme, ee).add(), loop=current_loop)
        return jsonify({}), 204

    @app.route("/api/elvis")
    def elvis():
        asyncio.ensure_future(
            non_ws_sytem_commands["elvis"].add(Message(CommandType.elvis, "")),
            loop=current_loop,
        )
        return jsonify({}), 204

    @app.route("/api/ceiling-lights-toggle")
    def ceiling_lights_toggle():
        print("\033[34mRurning toggle ceiling lights.\033[0m")
        home_assistant.toggle_ceiling_lights()
        return jsonify({}), 204

    @app.route("/api/lights-red")
    def lights_red():
        print("\033[34mSetting lights to red.\033[0m")
        home_assistant.set_lights_red()
        return jsonify({}), 204

    while True:
        await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(main())
