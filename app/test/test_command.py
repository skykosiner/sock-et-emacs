import sys

sys.path.append("..")

import unittest

from command import Command
from message import CommandType, Message
from get_status import get_status
from get_data import get_data


class TestCommandClass(unittest.TestCase):
    def test_vim_insert(self):
        command = Command()
        data = Message(CommandType.vim_insert, "!vi deez nuts")
        data.message = data.message_without_command()

        buffer = (
            command.set_type(data.command)
            .set_status(get_status(data.command, data))
            .set_data(get_data(type=data.command, msg=data))
            .buffer
        )
        decoded_stauts = buffer[:52].decode("ascii").replace("\x00", "")
        decoded_msg= buffer[52:].decode("ascii").replace("\x00", "")


        self.assertIs(buffer[0], 0, "It's so over, the type isn't correct.")
        self.assertTrue(
            decoded_stauts == "Inserted: deez nuts", "It's Joever. Buffer status isn't correct."
        )
        self.assertTrue(
            decoded_msg == "norm ideez nuts", "It's Joever. Buffer data isn't correct."
        )

    def test_vim_after(self):
        command = Command()
        data = Message(CommandType.vim_after, "!va deez nuts")
        data.message = data.message_without_command()

        buffer = (
            command.set_type(data.command)
            .set_status(get_status(data.command, data))
            .set_data(get_data(type=data.command, msg=data))
            .buffer
        )
        decoded_stauts = buffer[1:52].decode("ascii").replace("\x00", "")
        decoded_msg = buffer[52:].decode("ascii").replace("\x00", "")

        self.assertIs(buffer[0], 1, "It's so over, the type isn't correct.")
        self.assertTrue(
            decoded_stauts == "Inserted: deez nuts", "It's Joever. Buffer status isn't correct."
        )
        self.assertTrue(
            decoded_msg == "norm adeez nuts", "It's Joever. Buffer data isn't correct."
        )

    def test_vim_command(self):
        command = Command()
        data = Message(CommandType.vim_command, "!vc J")
        data.message = data.message_without_command()

        buffer = (
            command.set_type(data.command)
            .set_status(get_status(data.command, data))
            .set_data(get_data(type=data.command, msg=data))
            .buffer
        )
        decoded_stauts = buffer[1:52].decode("ascii").replace("\x00", "")
        decoded_msg = buffer[52:].decode("ascii").replace("\x00", "")

        self.assertIs(buffer[0], 2, "It's so over, the type isn't correct.")
        self.assertTrue(
                decoded_stauts == "Vim Command: J", "It's Joever. Buffer status isn't correct."
        )
        self.assertTrue(
            decoded_msg == "norm J", "It's Joever. Buffer data isn't correct."
        )

    def test_vim_colors(self):
        command = Command()
        buffer = (
            command.set_type(CommandType.vim_colors)
            .set_status(get_status(CommandType.vim_colors, color="gruvbox"))
            .set_data(get_data(type=CommandType.vim_colors, color="gruvbox"))
            .buffer
        )
        decoded_stauts = buffer[1:52].decode("ascii").replace("\x00", "")
        decoded_msg = buffer[52:].decode("ascii").replace("\x00", "")

        self.assertIs(buffer[0], 3, "It's so over, vim color type isn't correct.")
        self.assertTrue(
                decoded_stauts == "Changing vim colors to: gruvbox", "Didn't get correct data back from buffer for status"
        )
        self.assertTrue(
                decoded_msg == "silent colorschehme gruvbox", "Didn't get correct data back from buffer for status"
        )

    def test_system_command(self):
        command = Command()
        data = Message(CommandType.system_command, "asdf")
        buffer = (
            command.set_type(CommandType.system_command)
            .set_status(get_status(CommandType.system_command, data))
            .set_data(get_data(type=CommandType.system_command, cmd="setxkbmap -layout real-prog-dvorak"))
            .buffer
        )
        decoded_stauts = buffer[1:52].decode("ascii").replace("\x00", "")
        decoded_msg = buffer[52:].decode("ascii").replace("\x00", "")

        self.assertIs(buffer[0], 4, "It's so over, sytsem type isn't correct.")
        self.assertTrue(
                decoded_stauts == "asdf", "Didn't get correct data back from buffer for status"
        )
        self.assertTrue(
                decoded_msg == "silent! !setxkbmap -layout real-prog-dvorak", "Didn't get correct data back from buffer for status"
        )

    def test_elvis_command(self):
        command = Command()
        buffer = (
            command.set_type(CommandType.elvis)
            .set_status(get_status(CommandType.elvis))
            .set_data(get_data(type=CommandType.elvis, cmd="/home/sky/.local/bin/elvis"))
            .buffer
        )

        decoded_stauts = buffer[1:52].decode("ascii").replace("\x00", "")
        decoded_msg = buffer[52:].decode("ascii").replace("\x00", "")
        self.assertIs(buffer[0], 5, "It's so over, Elvis type isn't correct.")
        self.assertTrue(
                decoded_stauts == "RUNNING ELVIS", "Didn't get correct data back from buffer for status"
        )
        self.assertTrue(
                decoded_msg == "silent! !/home/sky/.local/bin/elvis", "Didn't get correct data back from buffer for status"
        )

    def test_change_font(self):
        command = Command()
        buffer = (
            command.set_type(CommandType.change_font)
            .set_status(get_status(type=CommandType.change_font, font="UbuntuMono Nerd Font"))
            .set_data(get_data(type=CommandType.change_font, font="UbuntuMono Nerd Font"))
            .buffer
        )

        decoded_stauts = buffer[1:52].decode("ascii").replace("\x00", "")
        decoded_msg = buffer[52:].decode("ascii").replace("\x00", "")
        self.assertIs(buffer[0], 6, "It's so over, vim color type isn't correct.")
        self.assertTrue(
                decoded_stauts == "Setting font to: UbuntuMono Nerd Font", "Didn't get correct data back from buffer for status"
        )
        self.assertTrue(
                decoded_msg == "silent !sed -i 's/font_family .*/font_family UbuntuMono Nerd Font/g' ~/.config/kitty/kitty.conf && xdotool key ctrl+shift+F5", "Didn't get correct data back from buffer for status"
        )
