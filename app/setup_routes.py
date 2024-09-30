import asyncio

from flask import Flask, jsonify
from homeassitant import HomeAssistant
from message import CommandType, Message
from change_font import ChangeFontRandom
from system_command import SystemCommand
from pyee.asyncio import AsyncIOEventEmitter
from vim_colorscheme import VimColorScheme, random_color


def setup_routes(
    app: Flask,
    current_loop: asyncio.AbstractEventLoop,
    ee: AsyncIOEventEmitter,
    home_assistant: HomeAssistant,
):
    non_ws_sytem_commands = {
        "elvis": SystemCommand("/home/sky/.local/bin/elvis", "", 0, ee),
    }

    @app.route("/api/change-vim-color")
    def change_vim_color():
        asyncio.ensure_future(
            VimColorScheme(random_color(), ee).add(), loop=current_loop
        )
        return jsonify({}), 204

    @app.route("/api/change-font")
    def change_font_route():
        asyncio.ensure_future(ChangeFontRandom(ee).add(), loop=current_loop)
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
