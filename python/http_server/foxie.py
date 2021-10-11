import asyncio

import aiohttp
from threading import Lock

async def main():
    async def req():
        async with aiohttp.ClientSession() as session:
            async with session.get('http://0.0.0.0:8000/') as resp:
                return await resp.text()

    chickens = await asyncio.gather(*[req() for _ in range(20)])
    print(chickens)


if __name__ == '__main__':
    asyncio.run(main())
