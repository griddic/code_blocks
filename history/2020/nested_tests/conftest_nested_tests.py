from contextlib import contextmanager

import pytest

from reporter import Reporter


class Subtests:
    class SubtestsCollection:
        def __init__(self, subtests):
            self._subtests = subtests
            self._errors = []
            self._failed_subtests = []

        @contextmanager
        def test(self, subtest_id):
            if self._subtests.subtest_wrapper_creator:
                wrapper = self._subtests.subtest_wrapper_creator(subtest_id)
            else:
                @contextmanager
                def wrapper():
                    yield
            with self._subtests.original.test(subtest_id):
                with wrapper():
                    try:
                        yield
                    except Exception as e:
                        self._failed_subtests.append(subtest_id)
                        self._errors.append(e)
                        raise

        def check(self):
            if self._errors:
                msg = '\n'.join(list(map(str, zip(self._failed_subtests, map(str, self._errors)))))
                msg = 'Subtests failed:\n' + msg
                raise AssertionError(msg) from self._errors[-1]

    def __init__(self, original, *, subtest_wrapper_creator=None):
        self._subtest_wrapper_creator = subtest_wrapper_creator
        self._collection = None
        self.original = original

    @property
    def subtest_wrapper_creator(self):
        return self._subtest_wrapper_creator

    def __enter__(self):
        if self._collection:
            raise Exception('Reusing of Subtests is forbidden.')
        self._collection = self.SubtestsCollection(self)
        return self._collection

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._collection.check()


@pytest.fixture
def nested_tests(subtests, reporter: Reporter, logger):
    def wrapper_creator(subtest_id):
        @contextmanager
        def wrapper():
            with reporter.step(f'Subtest: {subtest_id}'):
                try:
                    yield
                except Exception as e:
                    logger.exception(str(e))
                    raise

        return wrapper

    def create_batch():
        return Subtests(subtests, subtest_wrapper_creator=wrapper_creator)

    return create_batch
