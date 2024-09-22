from message import CommandType, Message

def get_data(data: Message) -> bytes:
    type = data.command
    out = ""

    match type:
        case CommandType.vim_insert:
            out = f"norm i{data.message_without_command()}"
        case CommandType.vim_after:
            out = f"norm a{data.message_without_command()}"
        case CommandType.vim_command:
            out = f"norm {data.message_without_command()}"


    return bytes(out, "ascii")
