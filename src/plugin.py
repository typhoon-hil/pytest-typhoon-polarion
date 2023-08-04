import pytest
from polarion import polarion
from .runtime_settings import TestExecutionResult, Settings
from .exceptions import PolarionTestIDWarn

Settings.POLARION_HOST = 'http://localhost:80/polarion'
Settings.POLARION_USER = 'admin'
Settings.POLARION_PASSWORD = 'admin'

# TODO: [DOCUMENTATION] To create a token (Valid for maximum 90 days)
# Show Settings (Engine below the Pn symbol in the left-up corner)
# > My Account > Personal Access Token (upper-center, below the page header)
Settings.POLARION_TOKEN = "eyJraWQiOiJiZmFiMGYyZS1jMGE4MDIxNy0zYzQ2NGZiNy00ZjRkNWEwOSIsInR5cCI6IkpXVCIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiJhZG1pbiIsImlkIjoiYmZhYzE5NDgtYzBhODAyMTctM2M0NjRmYjctOTkzMzY5M2YiLCJleHAiOjE2OTg4Nzk2MDAsImlhdCI6MTY5MTEzNzg3NH0.YN8i8YrMYcmRzla_7_92UJQ9hvOGJ9RiRgBlS5WEzigjoUgzqZswU-K2Y0R5vbEcLccDvsSHzzQQueHzNGq4zIOjzE9H74VMTFIBIPlm6oTSroILFBKFASlNdie27qnbMh4WmjFQCqiu2kHS5EgCbKqVUst8yxDMihJhfd7t92ZvcPp-YVxr0T8D7qgBqF77_9Mi20thlah3GN8YLA7UCQLFvI4JXn_hq2MCQABLUpl8CvMyATHp1AMjZOPMkDy70q9Nt_xBJZ2MoPGwiY5F4DKQ48f0PGs8ywIImRbDL1frGlphix8KFzEWnWJ0rGRulN_TL_bNYtJJquYWiE3tSw"


import logging
logger = logging.getLogger(__file__)

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
    if _authentication() == "PASS_AUTH":  # Password Authentication
        client = polarion.Polarion(polarion_url=Settings.POLARION_HOST,
                                   user=Settings.POLARION_USER,
                                   password=Settings.POLARION_PASSWORD)
    else:  # TOKEN_AUTH
        client = polarion.Polarion(polarion_url=Settings.POLARION_HOST,
                                   user=Settings.POLARION_USER,
                                   token=Settings.POLARION_TOKEN)

    project = client.getProject(Settings.POLARION_PROJECT_ID)

    run = project.getTestRun(Settings.POLARION_TEST_RUN)

    for key, item in TestExecutionResult.polarion_id_test_result.items():
        print(key, item)

    print("End of pytest_terminal_summary")
    print()


def pytest_sessionfinish(session):
    pass


def _fill_keys(stats, outcome):
    """Provides a dictionary with the polarion tags and the test result for uploading in polarion app.
    Used in ``pytest_terminal_summary`` hook."""
    if outcome in stats:
        for stat in stats[outcome]:
            try:
                polarion_test_id = TestExecutionResult.polarion_tags[stat.nodeid]
            except KeyError:
                continue
            try:
                TestExecutionResult.polarion_id_test_result[polarion_test_id].append(stat)
            except KeyError:
                TestExecutionResult.polarion_id_test_result[polarion_test_id] = [stat]


def _get_polarion_marker(item):
    """Catches the polarion marker.
    Used in ``_store_item`` function > ``pytest_collection_modifyitems`` hook"""
    return item.get_closest_marker('polarion')


def _store_item(item):
    """On colletion storage the tests node and the polarion tags.
    Used in ``pytest_collection_modifyitems`` hook"""
    marker = _get_polarion_marker(item)
    if not marker:
        return

    test_id = marker.kwargs['test_id']
    TestExecutionResult.polarion_tags[item.nodeid] = test_id


def _authentication():
    """Define if the authentication will be done by token or password.
    Used in ``pytest_terminal_summary`` hook"""
    if Settings.POLARION_TOKEN == "":
        logger.info("Trying Polarion auth by Token")
        return "PASS_AUTH"
    else:
        logger.info("Trying Polarion auth by Password")
        return "TOKEN_AUTH"
