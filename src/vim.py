from dataclasses import dataclass
from message import CommandType, Message

@dataclass
class IsGoodVim:
    is_good: bool
    error: str

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

def insert(input: str) -> str:
    for char in list(input):
        ascii_code = ord(char)
        if ascii_code < 32 or ascii_code > 127:
            return f"Inavlid ascii char {char}.... How did that even happen?"

    if len(input) > 5:
        input = input[:5]


    return ""

def vim_command(command: str) -> str:
    if vim_commands.__contains__(command):
        return ""

    return f"The command {command} is not a valid command."

def validate_vim_command(data: Message) -> IsGoodVim:
    error = ""
    command_type = data.command
    if command_type == CommandType.vim_insert or command_type == CommandType.vim_after:
        error = insert(data.message_without_command())
        print(error)
    elif command_type == CommandType.vim_command:
        error = vim_command(data.message_without_command())

    if len(error) > 0:
        return IsGoodVim(is_good=False, error=error)

    return IsGoodVim(is_good=True, error=None)
