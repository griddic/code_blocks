# pylint: disable=unused-argument
import pytest
from _pytest.config import create_terminal_writer
from random import Random

pytest_plugins = ['conftest_nested_tests']


@pytest.fixture
def logger(request):
    logger = logging.getLogger(request.node.nodeid)
    logger.setLevel(logging.DEBUG)
    logs = StringIO()
    handler = logging.StreamHandler(logs)
    handler.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
    logger.addHandler(handler)
    logger.oztqa_root = True
    yield logger
    allure.attach('logs', logs.getvalue())
    logger.removeHandler(handler)


@pytest.fixture(autouse=True)
def reporter(allure_dsl, request, browser, logger, debug):
    reporter_ = Reporter(browser, request.node.nodeid, allure_dsl, logger, debug=debug)
    try:
        yield reporter_
    finally:
        logger.info(f'Current url is: {browser.current_url}')
        reporter_.screenshot()
