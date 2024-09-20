from dataclasses import dataclass
from enum import Enum

class Command(Enum):
    vim_insert = 0
    vim_after = 1
    vim_command = 2
    system_command = 3

@dataclass
class Message:
    command: Command
    message: str

    def to_dict(self):
        return {
            "command": self.command,
            "message": self.message
        }

    @classmethod
    def from_dict(cls, data):
        command = Command[data['command']]  # Convert string back to enum
        return cls(command=command, message=data['message'])
