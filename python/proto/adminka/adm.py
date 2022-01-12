import logging
import threading
import time
import typing
from contextlib import contextmanager

import grpc
import gen.pb_python.admin_pb2 as admin_pb2
import gen.pb_python.admin_pb2_grpc as admin_pb2_grpc
from grpc_reflection.v1alpha import reflection
import concurrent.futures as futures


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


class LogLevelController:
    default_interval = 10 * 60

    def __init__(self, permanent_log_level):
        self.permanent_log_level = permanent_log_level
        self.reset_level_at = time.time()
        self.lock = threading.Lock()
        self._thread = None
        self._termination_event: threading.Event = None

    @property
    def _customized(self):
        return self.permanent_log_level != logging.root.level

    def set_level(self, level, duration=default_interval):
        with self.lock:
            self.reset_level_at = time.time() + int(duration)
            logging.root.setLevel(level)
            logging.warning(f'logging level is set to {_repr_level(level)}')

    def _start(self):

        while not self._termination_event.is_set():
            if self._customized:
                if self.reset_level_at < time.time():
                    with self.lock:
                        logging.root.setLevel(self.permanent_log_level)
                        logging.warning(f'logging level reset to permanent: {_repr_level(self.permanent_log_level)}')
            self._termination_event.wait(60)

    def reset(self):
        with self.lock:
            self.reset_level_at = time.time()
            logging.root.setLevel(self.permanent_log_level)
            logging.warning(f'reset logging settings {_repr_level(self.permanent_log_level)}')

    def __enter__(self):
        self._termination_event = threading.Event()
        self._thread = threading.Thread(target=self._start)
        self._thread.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._termination_event.set()
        self._thread.join()


class Admin(admin_pb2_grpc.AdminServicer):
    def __init__(self, permanent_log_level):
        self._log_level_controller = LogLevelController(permanent_log_level)

    def __enter__(self):
        self._log_level_controller.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._log_level_controller.__exit__(exc_type, exc_val, exc_tb)

    def SetLogLevel(self, request: admin_pb2.SetLogLevelRequests, context):
        """
        grpcurl -plaintext -d '{"level": "DEBUG", "duration": 30}' localhost:50055 Admin/SetLogLevel
        """
        level = _parse_level(request.level)
        duration = request.duration or self._log_level_controller.default_interval
        self._log_level_controller.set_level(level, duration)
        return admin_pb2.LogLevelState(
            current_level=str(_repr_level(logging.root.level)),
            permanent_log_level=str(_repr_level(self._log_level_controller.permanent_log_level)),
            seconds_to_reset_level=max(-1, int(self._log_level_controller.reset_level_at - time.time()))
        )

    def GetLogLevel(self, request: admin_pb2.GetLogLevelRequest, context):
        """
        grpcurl -plaintext localhost:50055 Admin/GetLogLevel
        """
        return admin_pb2.LogLevelState(
            current_level=str(_repr_level(logging.root.level)),
            permanent_log_level=str(_repr_level(self._log_level_controller.permanent_log_level)),
            seconds_to_reset_level=max(-1, int(self._log_level_controller.reset_level_at - time.time()))
        )

    def ResetLogLevel(self, request, context):
        """
        grpcurl -plaintext localhost:50055 Admin/ResetLogLevel
        """
        self._log_level_controller.reset()
        return admin_pb2.LogLevelState(
            current_level=str(_repr_level(logging.root.level)),
            permanent_log_level=str(_repr_level(self._log_level_controller.permanent_log_level)),
            seconds_to_reset_level=max(-1, int(self._log_level_controller.reset_level_at - time.time()))
        )


@contextmanager
def adminized(permanent_log_level):
    admin = grpc.server(futures.ThreadPoolExecutor())

    with Admin(permanent_log_level) as admin_servicer:
        admin_pb2_grpc.add_AdminServicer_to_server(admin_servicer, admin)
        admin.add_insecure_port('[::]:50055')

        names = [
            admin_pb2.DESCRIPTOR.services_by_name['Admin'].full_name,
            reflection.SERVICE_NAME,
        ]

        reflection.enable_server_reflection(names, admin)

        admin.start()

        try:
            yield
        finally:
            admin.stop(grace=None)
