import sys
sys.path.append("..")

import unittest

from command import Command
from message import CommandType, Message

class TestCommandClass(unittest.TestCase):
    def test_vim_insert(self):
        command = Command()
        data = Message(CommandType.vim_insert, "!vi deez nuts")

        buffer = command.set_type(data.command).set_data(bytes(data.message_without_command(), 'ascii')).buffer
        decoded_msg = buffer[1:].decode("ascii").replace("\x00", "")

        self.assertIs(buffer[0], 0, "It's so over, the type isn't correct.")
        self.assertTrue(decoded_msg == "deez nuts", "It's Joever. Buffer data isn't correct.")

    def test_vim_after(self):
        command = Command()
        data = Message(CommandType.vim_after, "!va deez nuts")

        buffer = command.set_type(data.command).set_data(bytes(data.message_without_command(), 'ascii')).buffer
        decoded_msg = buffer[1:].decode("ascii").replace("\x00", "")

        self.assertIs(buffer[0], 1, "It's so over, the type isn't correct.")
        self.assertTrue(decoded_msg == "deez nuts", "It's Joever. Buffer data isn't correct.")

    def test_vim_command(self):
        command = Command()
        data = Message(CommandType.vim_command, "!vc dd")

        buffer = command.set_type(data.command).set_data(bytes(data.message_without_command(), 'ascii')).buffer
        decoded_msg = buffer[1:].decode("ascii").replace("\x00", "")

        self.assertIs(buffer[0], 2, "It's so over, the type isn't correct.")
        self.assertTrue(decoded_msg == "dd", "It's Joever. Buffer data isn't correct.")

    def test_system_command(self):
        command = Command()
        data = Message(CommandType.system_command, "silent !i3 workspace 69")

        buffer = command.set_type(data.command).set_data(bytes(data.message, 'ascii')).buffer
        decoded_msg = buffer[1:].decode("ascii").replace("\x00", "")

        self.assertIs(buffer[0], 3, "It's so over, the type isn't correct.")
        self.assertTrue(decoded_msg == "silent !i3 workspace 69", "It's Joever. Buffer data isn't correct.")
