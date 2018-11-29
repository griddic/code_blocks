import logging
import os

import allure


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
"""
Following code is used to enable allure logging in tests.
Using it will afford you to have logic of interaction with testing object clear of allure.
So you will have both 
    allure reporting 
    and 
    an ability to reuse logic of interaction (API interface or Page Object) in non-test scripts.
"""

class LogToAllureHandler(logging.Handler):
    # noinspection PyMethodMayBeStatic
    def log(self, message):
        with allure.step(f'Log {message}'):
            pass

    def emit(self, record):
        self.log(f"({record.levelname}) {record.getMessage()}")


class AllureCatchLogs:
    def __init__(self):
        self.rootlogger = logging.getLogger()
        self.allurehandler = LogToAllureHandler()
        self.allurehandler.setLevel(logging.INFO)

    def __enter__(self):
        if self.allurehandler not in self.rootlogger.handlers:
            self.rootlogger.addHandler(self.allurehandler)

    def __exit__(self, exc_type, exc_value, traceback):
        self.rootlogger.removeHandler(self.allurehandler)


def allure_method_decorator(method):
    @allure.step(method.__name__)
    def wrapper(*args, **kwargs):
        with allure.step(f'Input for {method.__name__}'):
            allure.attach(str(args), name='args')
            allure.attach(str(kwargs), name='kwargs')
        returned = method(*args, **kwargs)
        allure.attach(str(returned), f'returned from {method.__name__}')
        return returned

    return wrapper


def add_allure_to_all_methods(cls):
    for attr in cls.__dict__:  # there's propably a better way to do this
        if isinstance(getattr(cls, attr), Callable):
            if attr.startswith("_"):
                continue
            setattr(cls, attr, allure_method_decorator(getattr(cls, attr)))
    return cls


add_allure_to_all_methods("SomeApiInterfaceInstance")



@pytest.fixture(scope="function", autouse=True)
def log_test(request):
    test_name = request.node.name
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    os.makedirs("logs", exist_ok=True)
    log_file_name = f'{test_name}.log'
    log_file_path = os.path.join("logs", log_file_name)
    if os.path.exists(log_file_path):
        os.remove(log_file_path)
    logging_to_allure_interceptor = LogToAllureHandler()
    logging_to_allure_interceptor.setLevel(logging.INFO)
    logger.addHandler(logging_to_allure_interceptor)
    yield
    logger.removeHandler(logging_to_allure_interceptor)

# ======================================================================================================================