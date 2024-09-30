#                1                  1-52               52-256
#     +-----------------------+--------------+------------------------+
#     |         type          /    status    /          data          |
#     +-----------------------+--------------+------------------------+
from message import CommandType


class Command:
    _type_idx = 0
    _status_idx = 1
    _data_idx = 52
    buffer: bytearray

    def __init__(self) -> None:
        self.buffer = bytearray(256)

    def reset(self):
        self.buffer = bytearray(256)
        return self

    def set_type(self, type: CommandType):
        self.buffer[self._type_idx] = type
        return self

    def set_status(self, data: bytes):
        assert len(data) <= 52, "\033[31mIt's Joever, status is over 52.\033[0m"
        self.buffer[self._status_idx : 52] = data
        return self

    def set_data(self, data: bytes):
        assert len(data) <= 204, print("\033[31mIt's Joever, data is over 127.\033[0m")
        self.buffer[self._data_idx : self._data_idx + len(data)] = data
        return self
