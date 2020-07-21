import logging
import os
from contextlib import contextmanager
from datetime import datetime
from io import StringIO

import pytz
from allure.constants import AttachmentType
from pytest_allure_dsl import allure
from selenium.webdriver.android.webdriver import WebDriver


class Reporter:
    # pylint: disable=too-many-arguments
    def __init__(self, browser: WebDriver, node_id, allure_dsl, logger, debug=False):
        self._browser = browser
        self._node_id = node_id
        self._logger = logger
        self._allure_dsl = allure_dsl
        self.debug = debug

    @property
    def _timestamp(self):
        return datetime.now(tz=pytz.timezone('Europe/Moscow')).isoformat()

    @property
    def tmpdir(self):
        path = os.path.join('.tmp', 'reporter', self._node_id)
        os.makedirs(path, exist_ok=True)
        return path

    def screenshot(self):
        file_name = f'{self._timestamp}.png'
        allure.attach(file_name, self._browser.get_screenshot_as_png(), AttachmentType.PNG)

    @contextmanager
    def attach_logs(self):
        logs = StringIO()
        handler = logging.StreamHandler(logs)
        handler.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
        self._logger.addHandler(handler)
        try:
            yield
        finally:
            allure.attach('logs', logs.getvalue())
            self._logger.removeHandler(handler)

    @contextmanager
    def dsl_step(self, *args, **kwargs):
        with self._allure_dsl.step(*args, **kwargs):
            with self.attach_logs():
                try:
                    yield
                    if self.debug:
                        self.screenshot()
                except Exception:
                    self.screenshot()
                    raise

    @contextmanager
    def step(self, *args, **kwargs):
        with allure.step(*args, **kwargs):
            with self.attach_logs():
                try:
                    yield
                    if self.debug:
                        self.screenshot()
                except Exception:
                    self.screenshot()
                    raise
