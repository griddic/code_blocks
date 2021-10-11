import random
import threading
import time
from functools import wraps
COUNTER = 0
COUNTER_LOCK = threading.Lock()


def counter_lock_decorator(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        with COUNTER_LOCK:
            return f(*args, **kwargs)

    return decorated


def inc():
    with COUNTER_LOCK:
        global COUNTER
        time.sleep(random.randint(0, 4))
        COUNTER += 1
        time.sleep(random.randint(0, 4))
        print(COUNTER)
        COUNTER -= 1


@counter_lock_decorator
def inc1():
    global COUNTER
    time.sleep(random.randint(0, 4))
    COUNTER += 1
    time.sleep(random.randint(0, 4))
    print(COUNTER)
    COUNTER -= 1


if __name__ == '__main__':
    ths = []
    for i in range(10):
        t = threading.Thread(target=inc)
        t.daemon = True
        ths.append(t)
        t.start()
    for t in ths:
        t.join()
