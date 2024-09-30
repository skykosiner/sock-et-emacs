from message import CommandType, Message


def get_status(
    type: CommandType,
    msg: Message | None = None,
    color: str | None = None,
    font: str | None = None,
) -> bytes:
    match type:
        case CommandType.vim_insert | CommandType.vim_after:
            assert msg is not None
            return bytes(f"Inserted: {msg.message}", "ascii")
        case CommandType.vim_command:
            assert msg is not None
            return bytes(f"Vim Command: {msg.message}", "ascii")
        case CommandType.system_command:
            assert msg is not None
            return bytes(f"{msg.message}", "ascii")
        case CommandType.elvis:
            return bytes("RUNNING ELVIS", "ascii")
        case CommandType.vim_colors:
            assert color is not None
            return bytes(f"Changing vim colors to: {color}", "ascii")
        case CommandType.change_font:
            assert font is not None
            return bytes(f"Setting font to: {font}", "ascii")
