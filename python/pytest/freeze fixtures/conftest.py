import os
import pickle


def construct_file_path(fixturedef, request):
    def replace_bad(rel_path):
        for ch in '<>:"/\\|?*':
            rel_path = rel_path.replace(ch, '_')
        return rel_path
    folder = os.path.join(request.config.cache._cachedir, '_frozen_fixtures',
                          replace_bad(request.node.nodeid), replace_bad(fixturedef.baseid))
    os.makedirs(folder, exist_ok=True)
    file_path = os.path.join(folder, replace_bad(fixturedef.argname) + '.pickle')

    return file_path


def pytest_fixture_setup(fixturedef, request):
    file_path = construct_file_path(fixturedef, request)
    if not os.path.exists(file_path):
        return
    with open(file_path, 'rb') as inn:
        value = pickle.load(inn)
    my_cache_key = request.param_index
    fixturedef.cached_result = (value, my_cache_key, None)
    return value


def pytest_fixture_post_finalizer(fixturedef, request):
    if not request.node.nodeid:
        return
    if getattr(fixturedef, 'cached_result', None) is None:
        return
    file_path = construct_file_path(fixturedef, request)
    with open(file_path, 'wb') as outt:
        pickle.dump(fixturedef.cached_result[0], outt)
