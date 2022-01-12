import json
import logging
from copy import copy
from datetime import datetime
from functools import lru_cache

from structlog import get_logger
from structlog.types import WrappedLogger


class UaHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        data = {
            'timestamp': datetime.utcnow().isoformat(),
            'level': record.levelname,
            'msg': record.msg,
            'stack': record.name,
        }
        data.update(getattr(record, 'binded', {}))
        print(json.dumps(data))


class _Logan(logging.Logger):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._binded = {}

    def bind(self, k, v):
        self._binded[k] = v

    def getChild(self, suffix: str):
        child = logging.Logger.getChild(self, suffix)
        child._binded = copy(self._binded)
        return child

    def clone(self):
        _clone = self.manager.getLogger(self.name)
        _clone._binded = copy(self._binded)
        return _clone

    def makeRecord(self, name, level, fn, lno, msg, args, exc_info,
                   func=None, extra=None, sinfo=None):
        record = super().makeRecord(name, level, fn, lno, msg, args, exc_info, func, extra, sinfo)
        # record.msg = json.dumps(dict(**self._binded, msg=record.msg))
        record.binded = self._binded
        return record


@lru_cache()
def main_logger() -> _Logan:
    # logging.root._binded = {}
    # logging.root.handlers = [UaHandler()]
    # logging.root.getChild = _Logan.getChild
    # logging.Logger.root = logging.root
    # logging.Logger.manager = logging.Manager(logging.root)
    logging.Logger.manager.setLoggerClass(_Logan)
    l = logging.getLogger('loadtesting')
    l.addHandler(UaHandler())
    return l


# def rootLogan():
#     logging.basicConfig()
#     return _Logan("root", logging.DEBUG)


def struct():
    log: WrappedLogger = get_logger()
    log = log.bind(user='anonymous', some_key=23)
    log = log.bind(user='hynek', another_key=42)
    log.info('user.logged_in', happy=True)


def own():
    logging.basicConfig()
    l: _Logan = main_logger()
    l.setLevel(logging.DEBUG)
    l.bind('server', "load")
    l.info('with binded')
    ll = l.getChild('slave')
    ll.bind('slave', 'specific')
    ll.info('slave say')
    l.warning('master again')



if __name__ == '__main__':
    own()
    logging.info()
