import asyncio
import threading
import time
import typing
from datetime import datetime
from functools import lru_cache, cached_property
from pathlib import Path

from aiohttp import web
import logging

LLC = 'log level controller'


class LogLevelController:
    default_level = logging.WARNING
    default_interval = 10 * 60

    def __init__(self):
        self.reset_level_at = time.time()
        self.lock = asyncio.Lock()
        self._start()

    @property
    def _customized(self):
        return self.default_level == logging.root.level

    async def set_level(self, level, duration=default_interval):
        async with self.lock:
            self.reset_level_at = time.time() + duration
            logging.root.setLevel(level)

    def _start(self):
        async def controller(llc: LogLevelController):
            while True:
                if llc._customized:
                    if llc.reset_level_at < time.time():
                        async with llc.lock:
                            logging.root.setLevel(llc.default_level)
                await asyncio.sleep(60)

        loop = asyncio.get_event_loop()
        loop.create_task(controller(self))

    async def reset(self):
        async with self.lock:
            self.reset_level_at = time.time()
            logging.root.setLevel(self.default_level)


@lru_cache()
def log_level_controller() -> LogLevelController:
    return LogLevelController()


def _parse_level(level: typing.Union[str, int]):
    try:
        return int(level)
    except ValueError:
        return logging._nameToLevel[level.upper()]


def _repr_level(level: int) -> typing.Union[str, int]:
    try:
        return logging._levelToName(level)
    except KeyError:
        return level


async def set_level(request: web.Request):
    level = _parse_level(request.match_info['level'])

    duration = request.match_info['duration']
    llc: LogLevelController = request.app[LLC]

    await llc.set_level(level, duration)
    return web.Response(text=f"""
    level = {_repr_level(logging.root.level)}
    reset in {llc.reset_level_at - time.time()} seconds
    """)


async def reset_level(request: web.Request):
    llc: LogLevelController = request.app[LLC]
    await llc.reset()
    return web.Response(text=f"""
    actual level: {_repr_level(logging.root.level)}
    default level: {_repr_level(llc.default_level)}
    """)


async def get_level(request: web.Request):
    return web.Response(text=str(_repr_level(logging.root.level)))


def create_app():
    app = web.Application()
    app[LLC] = log_level_controller()
    app.add_routes([web.get('/log/level/set/{level}/{duration}', set_level)])
    return app


async def start(app):
    print("starting")
    web.run_app(app, port=3333)


async def main():
    app = create_app()
    running = start(app)

    print("Огогошечки!")
    while i := input():
        print(i)

    await running

if __name__ == '__main__':
    asyncio.run(main())