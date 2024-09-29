from dataclasses import dataclass
from message import CommandType, Message


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
    "I",
    "J",
    "u",
]


def insert(input: str, error_dict: dict) -> str:
    for char in list(input):
        ascii_code = ord(char)
        if ascii_code < 32 or ascii_code > 127:
            error_dict["error"] = (
                f"Invalid ASCII char {char}.... How did that even happen?"
            )
            return input

    if len(input) > 5:
        input = input[:5]

    return input


def vim_command(command: str, error_dict: dict) -> None:
    if command not in vim_commands:
        error_dict["error"] = f"The command {command} is not a valid command."


def validate_vim_command(data: Message) -> IsGoodVim:
    error_dict = {"error": None}

    command_type = data.command
    if command_type in (CommandType.vim_insert, CommandType.vim_after):
        data.message = insert(data.message, error_dict)
    elif command_type == CommandType.vim_command:
        vim_command(data.message, error_dict)

    return IsGoodVim(is_good=error_dict["error"] is None, error=error_dict["error"])
