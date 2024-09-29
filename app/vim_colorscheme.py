import asyncio
from asyncio.tasks import Task
from pyee.asyncio import AsyncIOEventEmitter

from utils import current_vim_color_scheme

class VimColorScheme:
    stop_time: float = 0
    timer: int = 5
    current: str = current_vim_color_scheme()
    task: None | Task = None

    def __init__(self, set_color: str, ee: AsyncIOEventEmitter) -> None:
        self.set_color = set_color
        self.ee = ee

    async def add(self) -> None:
        now = asyncio.get_event_loop().time()
        if now > self.stop_time:
            self.ee.emit("vim-color", self.set_color)
            await self.start_timer()
            self.stop_time = now + self.timer

    async def start_timer(self):
        if self.task is not None:
            self.task.cancel()

        async def timer_task():
            await asyncio.sleep(self.timer)
            self.ee.emit("vim-color", self.current)

        self.task = asyncio.create_task(timer_task())
