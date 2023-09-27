import pytest
from polarion.polarion import Polarion
from polarion.record import Record
from polarion.workitem import Workitem
from zeep.exceptions import Fault
import logging
from .runtime_settings import TestExecutionResult, Settings, PolarionTestRunRefs
from .utils import read_or_get
from .exceptions import InvalidCredentialsError, TestCaseTypeError, TestCaseNotFoundError
from .work_items_utils import get_uid_values

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
    group.addoption(
        '--web-url',
        dest='web_url',
        help='Web link to be added to the test execution report'
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


@pytest.fixture
def web_url(request):
    return request.config.option.web_url


def pytest_configure(config):
    config.addinivalue_line(
        'markers',
        'polarion(test_id): ID register on Polarion for the test case available on the Test Run')

    Settings.POLARION_TEST_RUN = config.getoption("polarion_test_run")
    Settings.POLARION_PROJECT_ID = config.getoption("polarion_project_id")

    Settings.WEB_URL = config.getoption('web_url')
    Settings.ALLUREDIR = config.getoption('--alluredir')
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

    project = PolarionTestRunRefs.project
    run = PolarionTestRunRefs.run

    if Settings.WEB_URL is not None:

        import os
        from pathlib import Path

        full_alluredir = os.path.abspath(Settings.ALLUREDIR)
        html_path = Path(full_alluredir).parent / 'allure-html'

        print("html_path:", html_path)
        print("polarion_test_mapping:", TestExecutionResult.polarion_test_mapping)

        uid_values = get_uid_values(html_path)

        import sys
        sys.exit()

        # ...
    
    for test_case_id, test_results in TestExecutionResult.result_polarion_mapping.items():
        # TODO: Add parametrize and check how this works on XRAY Plugin
        polarion_result = polarion_assertion_selection(test_results[0])
        test_case_record = run.getTestCase(test_case_id)
        test_case_item = project.getWorkitem(test_case_id)

        try:
            test_case_record.setResult(polarion_result, "")
        except Fault as fault:
            if str(fault) == 'java.lang.UnsupportedOperationException':
                raise TestCaseTypeError(
                    'Test case result update failed. '
                    'Most probably because the test type was not '
                    'configured as "Automated Test".') from None
            else:
                raise e from None

        # Hyperlink on Test Case - Work Items 
        # Added if web-url is not NoneType
        if Settings.WEB_URL is not None:
            # - Remove all them and re-enter with Allure address
            test_node = test_results[0].nodeid
            test_case_links = test_case_item.hyperlinks

            # If hyperlink list is not empty it will be clean up
            if test_case_links is not None: 
                hyperlinks = _process_hyperlinks_from_polarion(test_case_links)
                for hyperlink in hyperlinks:
                    test_case_item.removeHyperlink(hyperlink)

            try:  # TODO: To temp fix when the test has multiple parameters
                test_rest_url = get_test_case_url(Settings.WEB_URL, test_node)  # On DEV
                test_case_item.addHyperlink(test_rest_url, Workitem.HyperlinkRoles.EXTERNAL_REF)
            except KeyError:
                pass


def pytest_sessionfinish(session):
    pass


def _fill_keys(stats, outcome):
    """Provides a dictionary with the polarion tags and the test result for uploading in polarion app.
    Used in ``pytest_terminal_summary`` hook."""
    if outcome in stats:
        for stat in stats[outcome]:
            try:
                polarion_test_id = TestExecutionResult.polarion_test_mapping[stat.nodeid]
            except KeyError:
                continue
            try:
                TestExecutionResult.result_polarion_mapping[polarion_test_id].append(stat)
            except KeyError:
                TestExecutionResult.result_polarion_mapping[polarion_test_id] = [stat]


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

    test_case_id = marker.kwargs['test_id']
    TestExecutionResult.polarion_test_mapping[item.nodeid] = test_case_id
    TestExecutionResult.test_polarion_mapping[test_case_id] = item.nodeid


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


def _process_hyperlinks_from_polarion(test_case_links):
    hyperlinks = []
    
    for hyperlink_item in test_case_links['Hyperlink']:
        hyperlinks.append(hyperlink_item['uri'])

    return hyperlinks
