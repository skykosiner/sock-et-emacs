from enum import Enum
from dataclasses import dataclass


class CommandType(Enum):
    vim_insert = 0
    vim_after = 1
    vim_command = 2
    vim_colors = 3
    system_command = 4
    elvis = 5
    change_font = 6
    home_assistant = 7

    def __index__(self):
        return self.value


@dataclass
class Message:
    command: CommandType
    message: str

    def message_without_command(self) -> str:
        return self.message[4:]
