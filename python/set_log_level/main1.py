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


class Signal:
    def __init__(self):
        self._set = False

    def is_set(self):
        return self._set

    def set(self):
        self._set = True


class LogLevelController:
    default_level = logging.WARNING
    default_interval = 10 * 60

    def __init__(self):
        self.reset_level_at = time.time()
        self.lock = asyncio.Lock()
        self._to_stop = False
        self._stopped = False


    @property
    def _customized(self):
        return self.default_level != logging.root.level

    async def set_level(self, level, duration=default_interval):
        async with self.lock:
            self.reset_level_at = time.time() + int(duration)
            logging.root.setLevel(level)

    async def start(self):
        logging.warning('Log level controller started.')
        try:
            while not self._to_stop:
                if self._customized:
                    if self.reset_level_at < time.time():
                        async with self.lock:
                            logging.root.setLevel(self.default_level)
                await asyncio.sleep(1)
        finally:
            logging.warning('Log level controller stopped.')
            self._stopped = True

    async def reset(self):
        async with self.lock:
            self.reset_level_at = time.time()
            logging.root.setLevel(self.default_level)

    def stop(self):
        logging.info("exiting from LLC")
        self._to_stop = True

    @property
    def stopped(self):
        return self._stopped


def _parse_level(level: typing.Union[str, int]):
    try:
        return int(level)
    except ValueError:
        return logging._nameToLevel[level.upper()]


def _repr_level(level: int) -> typing.Union[str, int]:
    try:
        return logging._levelToName[level]
    except KeyError:
        return level


async def set_level(request: web.Request):
    level = _parse_level(request.match_info['level'])

    duration = request.match_info.get('duration', LogLevelController.default_interval)
    llc: LogLevelController = request.app[LLC]

    await llc.set_level(level, duration)
    return web.Response(text=f"""
    level = {_repr_level(logging.root.level)}
    reset in {llc.reset_level_at - time.time()} seconds
    """)


async def get_level(request):
    return web.Response(text=str(_repr_level(logging.root.level)))


async def reset_level(request: web.Request):
    llc: LogLevelController = request.app[LLC]
    await llc.reset()
    return web.Response(text=f"""
    actual level: {_repr_level(logging.root.level)}
    default level: {_repr_level(llc.default_level)}
    """)


async def start_background_tasks(app):
    _llc = LogLevelController()
    app[LLC] = _llc
    app['redis_listener'] = asyncio.create_task(_llc.start())


async def cleanup_background_tasks(app):
    task : asyncio.Task = app['redis_listener']
    llc: LogLevelController = app[LLC]
    llc.stop()
    while not llc.stopped:
        await asyncio.sleep(1)

    task.cancel()
    await app['redis_listener']


def create_app():
    app = web.Application()
    app.on_startup.append(start_background_tasks)
    app.on_shutdown.append(cleanup_background_tasks)
    app.add_routes([web.get('/log/level/set/{level}/{duration}', set_level)])
    app.add_routes([web.get('/log/level/set/{level}', set_level)])
    app.add_routes([web.get('/log/level', get_level)])
    app.add_routes([web.get('/log/level/reset', reset_level)])
    return web.AppRunner(app)


class Callback:
    def __init__(self):
        self._callable = None
        self._do = False

    def register(self, callable):
        self._callable = callable

    def __call__(self):
        return self._callable.__call__()


def run_server(runner: web.AppRunner, stopper: Callback):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(runner.setup())
    site = web.TCPSite(runner, 'localhost', 8080)

    async def stop():
        logging.info("stopping site")
        await site.stop()
        logging.info("Stopping admins")
        await runner.shutdown()
        logging.info("cleaning")
        await runner.cleanup()
        logging.info("cleaned")
        loop.call_soon_threadsafe(loop.stop)

    stopper.register(stop)

    loop.run_until_complete(site.start())
    loop.run_forever()


async def run_async(stop: Signal):
    runner = create_app()
    await runner.setup()
    site = web.TCPSite(runner, 'localhost', 8080)
    await site.start()
    print("site started")
    while not stop.is_set():
        await asyncio.sleep(1)
    await asyncio.sleep(2)
    print("site stopping")
    # await site.stop()
    await runner.shutdown()
    # await runner.cleanup()


def run_sync(stop):
    asyncio.run(run_async(stop))


def main():
    logging.basicConfig()
    logging.root.setLevel(logging.DEBUG)
    app = create_app()
    stop = Callback()
    t = threading.Thread(target=run_server, args=(app, stop))
    t.start()
    logging.info("Огогошечки!")
    while i := input():
        print(i)
    asyncio.run(stop())
    print("stopped")
    t.join()
    # t.join()


if __name__ == '__main__':
    logging.basicConfig()
    logging.root.setLevel(logging.DEBUG)
    # asyncio.run_coroutine_threadsafe()

    stop = Signal()

    t = threading.Thread(target=run_sync, args=(stop,))
    t.start()

    while i := input():
        print(i)

    print("to stop")
    stop.set()
    t.join()
    print("stopped")
