from dataclasses import dataclass
from enum import Enum

class CommandType(Enum):
    vim_insert = 0
    vim_after = 1
    vim_command = 2
    system_command = 3
    elvis = 4

    def __index__(self):
        return self.value

@dataclass
class Message:
    command: CommandType
    message: str

    def message_without_command(self) -> str:
        return self.message[4:]
