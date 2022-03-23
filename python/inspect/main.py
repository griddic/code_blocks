import inspect
import logging
import sys


def lookup_logger(child_name=None):
    stack = []
    frame = inspect.currentframe()
    while frame:=frame.f_back:
        if _logger := frame.f_locals.get('logger', None):
            if isinstance(_logger, logging.Logger):
                if len(stack) == 0:
                    # идиотская ситуация, когда объявленна переменная logging, но хочется воспользоваться этой функцией
                    return _logger
                return _logger.getChild(child_name or '.'.join(stack[::-1]))
        if _self := frame.f_locals.get('self', None):
            try:
                # не хочу разбираться кто там из них будет обычным аттрибутом, кто пропертёй, кто дескриптором данных
                # поэтому https://docs.python.org/2/glossary.html#term-eafp
                _logger = _self.logger
            except AttributeError:
                pass
            else:
                if isinstance(_logger, logging.Logger):
                    return _logger.getChild(child_name or '.'.join(
                        [frame.f_code.co_name] + stack[::-1]
                    ))
        stack.append(frame.f_code.co_name)

    if len(stack) > 0:
        stack[-1] = 'root'  # show `root` instead or `<module>` startup
    return logging.root.getChild(child_name or '.'.join(stack[::-1]))


def inner(text='koko'):
    lookup_logger().info(text)


class Inner:
    def __init__(self):
        self.logger = logging.getLogger('class')

    def say(self):
        inner()
        lookup_logger().info('method in class with logger')


def foo():
    logging.basicConfig()
    logging.root.setLevel(logging.DEBUG)
    logger = logging.getLogger('func')
    logger.info('created')
    inner()
    i = Inner()
    i.say()

    lookup_logger().info('reuse global')


def main():
    foo()


if __name__ == '__main__':
    main()
    lookup_logger().info('from root')
    inner()
