import asyncio
from typing import Dict
from websocket import WebSocketApp
from pyee.asyncio import AsyncIOEventEmitter

from tcp import TCP
from command import Command
from get_data import get_data
from get_status import get_status
from vim import validate_vim_command
from message import CommandType, Message
from system_command import SystemCommand


def setup_listen_events(
    ee: AsyncIOEventEmitter,
    ws: WebSocketApp,
    tcp: TCP,
    system_commands: Dict[str, SystemCommand],
    current_loop: asyncio.AbstractEventLoop,
):
    command = Command()

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
            command.reset()
            .set_type(message.command)
            .set_status(get_status(type=message.command, msg=message))
            .set_data(get_data(type=message.command, msg=message))
            .buffer
        )
        tcp.send_all(buffer)
        print(f"\033[32mSendning vim {message.command} with {message.message}\033[0m")

    @ee.on("system-command")
    def system_command(cmd: str, message: Message, tcp=tcp) -> None:
        buffer = (
            command.reset()
            .set_type(message.command)
            .set_status(get_status(type=message.command, msg=message))
            .set_data(get_data(type=message.command, cmd=cmd))
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
        buffer = (
            command.reset()
            .set_type(CommandType.vim_colors)
            .set_status(get_status(CommandType.vim_colors, color=color))
            .set_data(get_data(CommandType.vim_colors, color=color))
            .buffer
        )

        tcp.send_all(buffer)
        print(f"\033[32mChanging vim colorscheme too {color}\033[0m")

    @ee.on("change-font")
    def change_font(font: str) -> None:
        buffer = (
            command.reset()
            .set_type(CommandType.change_font)
            .set_status(get_status(CommandType.change_font, font=font))
            .set_data(get_data(CommandType.change_font, font=font))
            .buffer
        )
        tcp.send_all(buffer)
