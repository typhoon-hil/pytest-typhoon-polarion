import pytest
from polarion import polarion
from .runtime_settings import TestExecutionResult, Settings
from .exceptions import PolarionTestIDWarn

Settings.POLARION_HOST = 'http://localhost:80/polarion'
Settings.POLARION_USER = 'admin'
Settings.POLARION_PASSWORD = 'admin'
# Settings.POLARION_TOKEN = ""
# Settings.POLARION_PROJECT_ID = 'ExampleProject'
# Settings.POLARION_TEST_RUN = ''


def pytest_addoption(parser):
    group = parser.getgroup('polarion')
    group.addoption(
        "--polarion-test-run",
        dest='polarion_test_run',
        help='Polarion test run id'
    )
    group.addoption(
        "--polarion-project-id",
        dest='polarion_project_id',
        help='Polarion project id'
    )


@pytest.fixture
def polarion_test_run(request):
    return request.config.option.polarion_test_run


@pytest.fixture
def polarion_project_id(request):
    return request.config.option.polarion_project_id


def pytest_configure(config):
    config.addinivalue_line(
        'markers',
        'polarion(test_id): ID register on Polarion for the test case available on the Test Run')

    Settings.POLARION_TEST_RUN = config.getoption("polarion_test_run")
    Settings.POLARION_PROJECT_ID = config.getoption("polarion_project_id")


def pytest_collection_modifyitems(config, items):
    for item in items:
        _store_item(item)


def pytest_terminal_summary(terminalreporter):
    _fill_keys(terminalreporter.stats, 'passed')
    _fill_keys(terminalreporter.stats, 'failed')
    _fill_keys(terminalreporter.stats, 'skipped')

    # Activate client and sync info
    print("Settings.POLARION_HOST", Settings.POLARION_HOST)
    print("Settings.POLARION_USER", Settings.POLARION_USER)
    print("Settings.POLARION_PASSWORD", Settings.POLARION_PASSWORD)
    client = polarion.Polarion(Settings.POLARION_HOST, Settings.POLARION_USER, Settings.POLARION_PASSWORD)

    project = client.getProject(Settings.POLARION_PROJECT_ID)

    run = project.getTestRun(Settings.POLARION_TEST_RUN)

    # pytest_to_polarion_test_cases = {
    #     'ExampleProject/test_plugin.py::test_sum': 'EP-392',
    #     'ExampleProject/test_plugin.py::test_square_root': 'EP-391',
    #     'aasnansnas': 'EP-300',
    # }

    for key, item in TestExecutionResult.polarion_tags.items():
        # print(item)
        print(key, item)
    #     try:
    #         test_case = run.getTestCase(item)
    #         if test_case is None:
    #             raise TypeError
    #         print("test_case.setResult(Record.ResultType.BLOCKED, 'Testing blocking')")
    #     # test_case.setResult(Record.ResultType.BLOCKED, 'Testing blocking')
    #     except TypeError as e:
    #         warnings.warn(f"Test ID {item} not founded in the selected Test Run Project!", PolarionTestIDWarn)
    #
    # print("Progressing ...")


def pytest_sessionfinish(session):
    pass


def _fill_keys(stats, outcome):
    if outcome in stats:
        for stat in stats[outcome]:
            try:
                xray_key = TestExecutionResult.polarion_tags[stat.nodeid]
            except KeyError:
                continue
            try:
                TestExecutionResult.polarion_id_test_result[xray_key].append(stat)
            except KeyError:
                TestExecutionResult.polarion_id_test_result[xray_key] = [stat]


def _get_polarion_marker(item):
    return item.get_closest_marker('polarion')


def _store_item(item):
    marker = _get_polarion_marker(item)
    if not marker:
        return

    test_id = marker.kwargs['test_id']
    TestExecutionResult.polarion_tags[item.nodeid] = test_id
