from dataclasses import dataclass
from message import Command, Message

@dataclass
class IsGoodVim:
    is_good: bool
    error: str | None

vim_commands = [
        "dd",
        "gg",
        "G",
        "h",
        "j",
        "k",
        "l",
        "o",
        "O",
        "zz",
        ">>",
        "<<",
        "_",
        "v",
        "V",
        "A",
        "I"
]

def insert(input: str) -> str | None:
    print(len(input))
    for char in input.split(""):
        ascii_code = ord(char)
        if ascii_code < 32 or ascii_code > 127:
            return f"Inavlid ascii char {char}.... How did that even happen?"

    if len(input) > 5:
        input = input[:5]

    return None

def vim_command(command: str) -> str | None:
    if vim_commands.__contains__(command):
        return None

    return f"The command {command} is not a valid command."

def validate_vim_command(data: Message) -> IsGoodVim:
    error = None
    command_type = data.command
    if command_type == Command.vim_insert or command_type == Command.vim_after:
        print(insert(data.message))
        error = insert(data.message)
    elif command_type == Command.vim_command:
        error = vim_command(data.message)

    if error:
        return IsGoodVim(is_good=False, error=error)

    return IsGoodVim(is_good=True, error=None)
