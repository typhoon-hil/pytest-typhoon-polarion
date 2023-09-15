import pytest
from polarion.polarion import Polarion
from polarion.record import Record
from zeep.exceptions import Fault
import logging
from .runtime_settings import TestExecutionResult, Settings, PolarionTestRunRefs
from .utils import read_or_get
from .exceptions import InvalidCredentialsError, TestCaseTypeError, TestCaseNotFoundError

logger = logging.getLogger(__file__)


def pytest_addoption(parser):
    group = parser.getgroup('polarion')
    group.addoption(
        "--secrets",
        dest='secrets',
        help='Login Information by the secrets file'
    )
    group.addoption(
        "--polarion-test-run",
        dest='polarion_test_run',
        help='Polarion Test Run ID'
    )
    group.addoption(
        "--polarion-project-id",
        dest='polarion_project_id',
        help='Polarion project id'
    )


@pytest.fixture
def secrets(request):
    return request.config.option.secrets


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

    secrets = config.getoption('secrets')

    Settings.POLARION_HOST = read_or_get(secrets, 'POLARION_HOST', '')
    Settings.POLARION_USER = read_or_get(secrets, 'POLARION_USER', '')
    Settings.POLARION_PASSWORD = read_or_get(secrets, 'POLARION_PASSWORD', '')
    Settings.POLARION_TOKEN = read_or_get(secrets, 'POLARION_TOKEN', '')

    logger.info(
        'Polarion Server configuration:\n'
        f'\tHost: {Settings.POLARION_HOST}\n'
        f'\tUser: {Settings.POLARION_USER}'
    )

    # Activate client and sync info
    try:
        if _authentication() == "PASS_AUTH":  # Password Authentication
            client = Polarion(
                polarion_url=Settings.POLARION_HOST,
                user=Settings.POLARION_USER,
                password=Settings.POLARION_PASSWORD)
        else:  # TOKEN_AUTH
            client = Polarion(
                polarion_url=Settings.POLARION_HOST,
                user=Settings.POLARION_USER,
                token=Settings.POLARION_TOKEN)
    except Exception as e:
        if str(e) == f'Could not log in to Polarion for user {Settings.POLARION_USER}' or \
            str(e) == 'Cannot login because WSDL has no SessionWebService':
            raise InvalidCredentialsError(
                'Your credentials are not valid, check your '
                '`secrets` file and make sure that host address '
                'user, and password or token is correct.'
                ) from None
        else:
            raise e from None

    project = client.getProject(Settings.POLARION_PROJECT_ID)
    run = project.getTestRun(Settings.POLARION_TEST_RUN)    
    
    # Add in a global class all the polarion test run references
    PolarionTestRunRefs.client = client
    PolarionTestRunRefs.project = project
    PolarionTestRunRefs.run = run


def pytest_collection_modifyitems(config, items):
    '''On this hook the Polarion Test ID markers is collected and organized in dictionaries. Also, 
    part of validation is made in order to not wait the whole test execution to discover that the 
    test results cannot be uploaded'''
    for item in items:
        _store_item(item)

    _validation_test_run() 


def pytest_terminal_summary(terminalreporter):
    _fill_keys(terminalreporter.stats, 'passed')
    _fill_keys(terminalreporter.stats, 'failed')
    _fill_keys(terminalreporter.stats, 'skipped')

    run = PolarionTestRunRefs.run

    for polarion_id, test_results in TestExecutionResult.polarion_id_test_result.items():
        # TODO: Add parametrize and check how this works on XRAY Plugin
        polarion_result = polarion_assertion_selection(test_results[0])
        test_case = run.getTestCase(polarion_id)
        try:
            test_case.setResult(polarion_result, "")
        except Fault as fault:
            if str(fault) == 'java.lang.UnsupportedOperationException':
                raise TestCaseTypeError(
                    'Test case result update failed. '
                    'Most probably because the test type was not '
                    'configured as "Automated Test".') from None
            else:
                raise e from None


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
    PolarionTestRunRefs.test_cases.append(marker.kwargs['test_id'])

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


def polarion_assertion_selection(result):
    if result.outcome == "passed":
        return Record.ResultType.PASSED
    elif result.outcome == "failed":
        return Record.ResultType.FAILED
    else:
        return Record.ResultType.BLOCKED


def _validation_test_run():
    run = PolarionTestRunRefs.run

    for test_case_id in PolarionTestRunRefs.test_cases:
        if not run.hasTestCase(test_case_id):
            raise TestCaseNotFoundError(
                f'The Test Case ID "{test_case_id}" was not found for the Test Run "{run.id}".'
            )

        if _test_type_select_from_test_case(test_case_id) != 'automated':
            raise TestCaseTypeError(
                f'The Test Case ID "{test_case_id}" is not configured as "Automated Test".'
            )


def _test_type_select_from_test_case(test_case_id):
    project = PolarionTestRunRefs.project
    test_case = project.getWorkitem(test_case_id)

    return test_case.customFields['Custom'][0]['value']['id']
