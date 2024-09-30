from message import CommandType, Message


def get_data(
    type: CommandType,
    msg: Message | None = None,
    cmd: str | None = None,
    color: str | None = None,
    font: str | None = None,
) -> bytes:
    match type:
        case CommandType.vim_insert:
            assert msg is not None, "HOW DID THIS HAPPEN"
            return bytes(f"norm i{msg.message}", "ascii")
        case CommandType.vim_after:
            assert msg is not None, "HOW DID THIS HAPPEN"
            return bytes(f"norm a{msg.message}", "ascii")
        case CommandType.vim_command:
            assert msg is not None, "HOW DID THIS HAPPEN"
            return bytes(f"norm {msg.message}", "ascii")
        case CommandType.vim_colors:
            assert color is not None, "COLOR IS NONE??"
            return bytes(f"silent colorscheme {color}", "ascii")
        case CommandType.system_command | CommandType.elvis:
            assert cmd is not None, "Command is none it's over."
            return bytes(f"silent! !{cmd}", "ascii")
        case CommandType.change_font:
            assert font is not None, "it's so over for font."
            return bytes(
                f"silent !sed -i 's/font_family .*/font_family {font}/g' ~/.config/kitty/kitty.conf && xdotool key ctrl+shift+F5",
                "ascii",
            )
