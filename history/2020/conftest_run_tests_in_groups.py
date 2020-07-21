def pytest_addoption(parser):
    group = parser.getgroup('split your tests into evenly sized groups and run them')
    group.addoption('--test-group-count', dest='test-group-count', type=int,
                    help='The number of groups to split the tests into')
    group.addoption('--test-group', dest='test-group', type=int,
                    help='The group of tests that should be executed')
    group.addoption('--test-group-random-seed', dest='random-seed', type=int,
                    help='Integer to seed pseudo-random test selection')


@pytest.hookimpl(hookwrapper=True)
def pytest_collection_modifyitems(session, config, items):
    yield
    group_count = config.getoption('test-group-count')
    group_id_natural = config.getoption('test-group')
    seed = config.getoption('random-seed')

    if (group_count is None) or (group_id_natural is None):
        return

    if group_id_natural < 1:
        raise ValueError('--test-group should be a positive integer. Indexing starting from 1.')
    if group_id_natural > group_count:
        raise ValueError(f"Can't get group {group_id_natural}. There only {group_count} specified.")

    group_id = group_id_natural - 1

    original_order = {item: index for index, item in enumerate(items)}

    if seed is not None:
        seeded = Random(seed)
        seeded.shuffle(items)

    items[:] = items[group_id::group_count]

    items.sort(key=original_order.__getitem__)

    terminal_reporter = config.pluginmanager.get_plugin('terminalreporter')
    if terminal_reporter is not None:
        terminal_writer = create_terminal_writer(config)
        message = terminal_writer.markup(
            '\nRunning test group #{0} ({1} tests)\n'.format(
                group_id_natural,
                len(items)
            ),
            yellow=True
        )
        terminal_reporter.write(message)
        # message = terminal_writer.markup(
        #     '\n'.join([item.name for item in items]) + '\n',
        #     yellow=True
        # )
        # terminal_reporter.write(message)
