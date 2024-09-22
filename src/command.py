#                    1                              2-128
#     +-----------------------------+---------------------------------+
#     |             type            |               data              |
#     +-----------------------------+---------------------------------+
import os
from message import CommandType

class Command:
    _type_idx = 0
    _data_idx = 1
    buffer: bytearray

    def __init__(self) -> None:
        self.buffer = bytearray(128)

    def reset(self):
        self.buffer = bytearray(128)
        return self

    def set_type(self, type: CommandType):
        self.buffer[self._type_idx] = type
        return self

    def set_data(self, data: bytes):
        if len(data) > 127:
            print("It's Joever, data is over 127.")
            os.error(-1)

        self.buffer[self._data_idx:self._data_idx+len(data)] = data

        return self
