import asyncio

from message import Message
from pyee.asyncio import AsyncIOEventEmitter


class SystemCommand:
    def __init__(
        self, start_command: str, stop_command: str, timer: int, ee: AsyncIOEventEmitter
    ) -> None:
        self.start_command = start_command
        self.stop_command = stop_command
        self.timer = timer
        self.ee = ee
        self.stop_time = 0
        self.task = None

    async def add(self, msg: Message) -> None:
        if len(self.stop_command) <= 0:
            self.ee.emit("system-command", self.start_command, msg)
            return

        now = asyncio.get_event_loop().time()
        if now > self.stop_time:
            self.ee.emit("system-command", self.start_command, msg)
            await self.start_timer(msg)
            self.stop_time = now + self.timer

    async def start_timer(self, msg: Message):
        if self.task is not None:
            self.task.cancel()

        async def timer_task():
            await asyncio.sleep(self.timer)
            self.ee.emit("system-command", self.stop_command, msg)

        self.task = asyncio.create_task(timer_task())
