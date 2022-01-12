import asyncio
import threading


async def back():
    while True:
        print('koko')
        await asyncio.sleep(5)

def wr():
    asyncio.run(back())


if __name__ == '__main__':
    t = threading.Thread(target=wr, daemon=True)
    t.start()
    while i := input():
        print(i)
