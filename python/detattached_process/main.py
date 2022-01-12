from multiprocessing import Process, Queue
from queue import Empty, Full


def f(queue_in: Queue, queue_out: Queue, stop: Queue):
    while True:
        try:
            stop.get_nowait()
            break
        except Empty:
            pass
        try:
            i = queue_in.get(timeout=1)
            print("kokoko")
            queue_out.put(f"processed {i}")
        except Empty:
            pass


if __name__ == '__main__':
    to_sub = Queue(maxsize=5)
    to_main = Queue(maxsize=3)
    stop = Queue()
    p = Process(target=f, args=(to_sub, to_main, stop))
    p.start()
    for i in range(10):
        try:
            to_sub.put(i, block=False)
        except Full:
            print('full')

    try:
        while True:
            try:
                o = to_main.get(timeout=1)
                print(o)
            except TimeoutError:
                pass
    except Empty:
        pass
    # print(q.get())    # prints "[42, None, 'hello']"
    print('stopping')
    stop.put(1)
    p.join()