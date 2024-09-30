import asyncio
import random
import subprocess

from asyncio.tasks import Task
from utils import current_font_kitty
from pyee.asyncio import AsyncIOEventEmitter


class ChangeFontRandom:
    stop_time: float = 0
    timer: int = 10
    current: str = current_font_kitty()
    task: None | Task = None
    fonts: list[str]

    def __init__(self, ee: AsyncIOEventEmitter) -> None:
        self.ee = ee
        self._get_fonts()

    def _get_fonts(self):
        output = subprocess.check_output(
            [
                "bash",
                "-c",
                "fc-list 2>/dev/null| grep -i 'Nerd' | awk -F: '{print $2}' | cut -d',' -f1 | sort | uniq",
            ]
        )
        self.fonts = list(
            filter(None, [font.strip() for font in output.decode().split("\n")])
        )

    async def add(self) -> None:
        now = asyncio.get_event_loop().time()
        if now > self.stop_time:
            self.ee.emit("change-font", random.choice(self.fonts))
            await self.start_timer()
            self.stop_time = now + self.timer

    async def start_timer(self):
        if self.task is not None:
            self.task.cancel()

        async def timer_task():
            await asyncio.sleep(self.timer)
            self.ee.emit("change-font", self.current)

        self.task = asyncio.create_task(timer_task())
