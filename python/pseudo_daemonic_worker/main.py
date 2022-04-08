# aka singleton implementation
import threading
import time

import requests


class PseudoDaemonic:
    data_provider = None
    host = None
    logger = None
    last_action_time = time.time()
    frequency = 10  # seconds
    lock = threading.Lock()

    @classmethod
    def setup(cls, data_provider, host, logger):
        cls.data_provider = data_provider
        cls.host = host
        cls.logger = logger

    @classmethod
    def do(cls):
        if cls.lock.locked():
            return "action is beeing performed right now"
        if time.time() - cls.last_action_time < cls.frequency:
            return "I'll do it later"

        t = threading.Thread(target=cls._do_blocking)
        t.start()
        return "action has been started in background"


    @classmethod
    def _do_blocking(cls):
        with cls.lock:
            # actual work here
            requests.post(cls.host, data=cls.data_provider.get())
