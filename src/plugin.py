import pytest
import os
from pathlib import Path
import numpy as np
from polarion.polarion import Polarion
from polarion.record import Record
from polarion.workitem import Workitem
from zeep.exceptions import Fault
import logging
# import logging.config

from .runtime_settings import (
    TestExecutionResult,
    Settings,
    PolarionTestRunRefs,
    Credentials
)
from .utils import read_or_get, read_or_get_ini
from .exceptions import InvalidCredentialsError, TestCaseTypeError, \
    TestCaseNotFoundError, ConfigurationError
from .work_items_utils import get_uid_values, get_test_case_url

logger = logging.getLogger(__file__)


def write_log(message, section=False, sub=True, type='a'):
    if Settings.ENABLE_LOG_FILE:
        from pathlib import Path
        if Settings.LOG_PATH is None:
            dir_path = Path().resolve()
        else:
            dir_path = Path(Settings.LOG_PATH).resolve()

        if section:
            pattern = "\n[{}]\n"
        elif sub:
            pattern = "\t{}\n"
        else:
            pattern = "{}\n"

        if isinstance(message, str):
            final_message = pattern.format(message)
        elif isinstance(message, list):
            final_message = ""
            for each in message:
                final_message += pattern.format(f"* {each}")

        with open((dir_path / "log_plugin.txt"), type) as ftxt:
            ftxt.write(final_message)


def pytest_addoption(parser):
    group = parser.getgroup('polarion')
    group.addoption(
        "--secrets",
        dest='secrets',
        help='Login Information by the secrets file'
    )
    group.addoption(
        "--config",
        dest='config_file',
        help='Configuration file for the plugin'
    )
    group.addoption(
        "--polarion-project-id",
        dest='polarion_project_id',
        help='Polarion project id'
    )
    group.addoption(
        "--polarion-test-run",
        dest='polarion_test_run',
        help='Polarion Test Run ID'
    )
    group.addoption(
        '--allow-comments',
        action="store_true",
        dest='allow_comments',
        help='Allow plugin to use work item comment to log test run information'
    )
    group.addoption(
        '--web-url',
        dest='web_url',
        help='Web link to be added to the test execution report'
    )
    # POLARION_VERSION
    group.addoption(
        '--log-plugin-report-path',
        dest='log_plugin_report',
        help='Allow a log file to be created on the path pass through this option'
    )


def pytest_configure(config: pytest.Config):
    config.addinivalue_line(
        'markers',
        'polarion(test_id): ID register on Polarion for the test case available on the Test Run')
    
    Settings.ALLUREDIR = config.getoption('--alluredir')

    secrets = config.getoption('secrets')
    config_file = config.getoption('config_file')
    opt_polarion_test_run = config.getoption("polarion_test_run")
    opt_polarion_project_id = config.getoption("polarion_project_id")

    write_log("pytest_configure", section=True, sub=False, type='w')
    write_log("Getting options:")
    write_log(f"* POLARION_TEST_RUN: {repr(opt_polarion_test_run)}")
    write_log(f"* POLARION_PROJECT_ID: {repr(opt_polarion_project_id)}")
    write_log(f"* WEB_URL: {repr(config.getoption('web_url'))}")
    write_log(f"* ALLOW_COMMENTS: {repr(config.getoption('allow_comments'))}\n")
    write_log(f"* secrets file: {repr(secrets)}")
    write_log(f"* config_file file: {repr(config_file)}\n")

    print("pytest_configure")
    print("Getting options:")
    print(f"* POLARION_TEST_RUN: {repr(opt_polarion_test_run)}")
    print(f"* POLARION_PROJECT_ID: {repr(opt_polarion_project_id)}")
    print(f"* WEB_URL: {repr(config.getoption('web_url'))}")
    print(f"* ALLOW_COMMENTS: {repr(config.getoption('allow_comments'))}\n")
    print(f"* secrets file: {repr(secrets)}")
    print(f"* config_file file: {repr(config_file)}\n")

    if secrets is None:
        raise ConfigurationError(
            '"secrets" files used by pytest-typhoon-polarion was not configured.\n'
            'In case the plugin is not needed uninstall the package using:\n'
            '\t"pip uninstall pytest-typhoon-polarion -y"')
    
    # From secrets file
    Credentials.POLARION_HOST = read_or_get(secrets, 'POLARION_HOST', '')
    Credentials.POLARION_USER = read_or_get(secrets, 'POLARION_USER', '')
    Credentials.POLARION_PASSWORD = read_or_get(secrets, 'POLARION_PASSWORD', '')
    Credentials.POLARION_TOKEN = read_or_get(secrets, 'POLARION_TOKEN', '')

    Settings.LOG_FILE_PATH = read_or_get_ini(config_file, 'LOG_FILE_PATH', config.getoption('log_plugin_report'), section="log_file")
    Settings.ENABLE_LOG_FILE = read_or_get_ini(config_file, 'ENABLE_LOG_FILE', False, section="log_file")

    if Settings.ENABLE_LOG_FILE:
        print(f"Config: Settings.LOG_PATH: {Settings.LOG_PATH}")
    else:
        print(f"Config: log_plugin file disabled.")

    Settings.POLARION_TEST_RUN = read_or_get_ini(config_file, 'POLARION_TEST_RUN', opt_polarion_test_run, section="polarion")
    Settings.POLARION_PROJECT_ID = read_or_get_ini(config_file, 'POLARION_PROJECT_ID', opt_polarion_project_id, section="polarion")
    Settings.POLARION_VERSION = read_or_get_ini(config_file, 'POLARION_VERSION', "2304", section="polarion")

    Settings.WEB_URL = read_or_get_ini(config_file, 'WEB_URL', config.getoption('web_url'), section='polarion') 
    Settings.ALLOW_COMMENTS = read_or_get_ini(config_file, 'ALLOW_COMMENTS', config.getoption('allow_comments'), section='polarion')
    
    Settings.ALLOW_COMMENTS = _validate_boolean_option(Settings.ALLOW_COMMENTS)
    
    Settings.POLARION_VERIFY_CERTIFICATE = read_or_get(secrets, 'POLARION_VERIFY_CERTIFICATE', "True")
    Settings.POLARION_VERIFY_CERTIFICATE = _validate_boolean_option(Settings.POLARION_VERIFY_CERTIFICATE)

    write_log("Secret file configurations set:")

    write_log(f"* Credentials.POLARION_HOST: {Credentials.POLARION_HOST} ({type(Credentials.POLARION_HOST)})")
    write_log(f"* Credentials.POLARION_USER: {Credentials.POLARION_USER} ({type(Credentials.POLARION_USER)})")
    write_log(f"* Credentials.POLARION_PASSWORD: {Credentials.POLARION_PASSWORD} ({type(Credentials.POLARION_PASSWORD)})")
    write_log(f"* Credentials.POLARION_TOKEN: {Credentials.POLARION_TOKEN} ({type(Credentials.POLARION_TOKEN)})")

    write_log(f"* Settings.POLARION_VERIFY_CERTIFICATE: {Settings.POLARION_VERIFY_CERTIFICATE} ({type(Settings.POLARION_VERIFY_CERTIFICATE)})")
    write_log(f"* Settings.POLARION_PROJECT_ID: {Settings.POLARION_PROJECT_ID} ({type(Settings.POLARION_PROJECT_ID)})")
    write_log(f"* Settings.POLARION_TEST_RUN: {Settings.POLARION_TEST_RUN} ({type(Settings.POLARION_TEST_RUN)})")

    write_log(f"* Settings.ALLOW_COMMENTS: {Settings.ALLOW_COMMENTS} ({type(Settings.ALLOW_COMMENTS)})")
    write_log(f"* Settings.WEB_URL: {Settings.WEB_URL} ({type(Settings.WEB_URL)})")
    write_log(f"* Settings.POLARION_VERSION: {Settings.POLARION_VERSION} ({type(Settings.POLARION_VERSION)})")

    # Activate client and sync info
    try:
        write_log(f"Authentication type used: {_authentication()}")
        if _authentication() == "PASS_AUTH":  # Password Authentication
            client = Polarion(
                polarion_url=Credentials.POLARION_HOST,
                user=Credentials.POLARION_USER,
                password=Credentials.POLARION_PASSWORD,
                verify_certificate=Settings.POLARION_VERIFY_CERTIFICATE)
        else:  # TOKEN_AUTH
            client = Polarion(
                polarion_url=Credentials.POLARION_HOST,
                user=Credentials.POLARION_USER,
                token=Credentials.POLARION_TOKEN,
                verify_certificate=Settings.POLARION_VERIFY_CERTIFICATE)

    except Exception as e:
        if str(e) == f'Could not log in to Polarion for user {Credentials.POLARION_USER}' or \
            str(e) == 'Cannot login because WSDL has no SessionWebService':
            write_log(
                f"Exception: {str(e)}: "
                'Your credentials are not valid, check your '
                '`secrets` file and make sure that host address '
                'user, and password or token is correct.'
            )
            raise InvalidCredentialsError(
                'Your credentials are not valid, check your '
                '`secrets` file and make sure that host address '
                'user, and password or token is correct.'
                ) from None
        else:
            write_log(f"Exception: {str(e)}")
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

    write_log("pytest_collection_modifyitems", section=True)
    write_log("Polarion Test Cases (based on the markers used):")
    write_log(PolarionTestRunRefs.test_cases)
    
    _validation_test_run()


def pytest_terminal_summary(terminalreporter):
    _fill_keys(terminalreporter.stats, 'passed')
    _fill_keys(terminalreporter.stats, 'failed')
    _fill_keys(terminalreporter.stats, 'skipped')

    project = PolarionTestRunRefs.project
    run = PolarionTestRunRefs.run

    if Settings.WEB_URL is not None:
        full_alluredir = os.path.abspath(Settings.ALLUREDIR)
        html_path = Path(full_alluredir).parent / 'allure-html'

        uid_test_mapping, parent_uid = get_uid_values(html_path)
        
        TestExecutionResult.uid_test_mapping = uid_test_mapping
        TestExecutionResult.parent_uid = parent_uid

    for test_case_id, test_results in TestExecutionResult.result_polarion_mapping.items():
        test_case_record = run.getTestCase(test_case_id)
        test_case_item = project.getWorkitem(test_case_id)

        # Hyperlink on Test Case - Work Items 
        # Added if web-url is not NoneType
        if Settings.WEB_URL is not None:
            # - Remove all them and re-enter with Allure address
            test_node = test_results[0].nodeid
            test_case_links = test_case_item.hyperlinks

            # If hyperlink list is not e409mpty it will be clean up
            if test_case_links is not None: 
                hyperlinks = _process_hyperlinks_from_polarion(test_case_links)
                for hyperlink in hyperlinks:
                    test_case_item.removeHyperlink(hyperlink)

            try:  # TODO: To temp fix when the test has multiple parameters
                test_rest_url = get_test_case_url(
                    Settings.WEB_URL, 
                    TestExecutionResult.parent_uid, 
                    TestExecutionResult.uid_test_mapping, 
                    test_node,
                )
                test_case_item.addHyperlink(test_rest_url, Workitem.HyperlinkRoles.EXTERNAL_REF)
            except KeyError as e:
                pass

        # TODO: Add parametrize and check how this works on XRAY Plugin
        if len(test_results) > 1:  # parametrize mark
            message, comment, polarion_result = polarion_assertion_selection_parametrize(test_results)
        else:
            message, comment, polarion_result = polarion_assertion_selection(test_results)

        if Settings.ALLOW_COMMENTS:
            test_case_item.addComment(message, comment)

        try:
            test_case_record.setResult(polarion_result, message)
        except Fault as fault:
            if str(fault) == 'java.lang.UnsupportedOperationException':
                raise TestCaseTypeError(
                    'Test case result update failed. '
                    'Most probably because the test type was not '
                    'configured as "Automated Test".') from None
            else:
                """
                The error "zeep.exceptions.Fault: com.polarion.core.util.exceptions.UserFriendlyRuntimeException: Sorry this action cannot be executed without providing an e-signature in the Polarion portal: Execution of a Test Case in the Test Run 'REL'."
                falls here when the Test Run is not configured as "Automated".
                """
                raise fault from None


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

    if not marker:
        return

    test_case_id = marker.kwargs['test_id']
    PolarionTestRunRefs.test_cases.append(test_case_id)
    TestExecutionResult.polarion_test_mapping[item.nodeid] = test_case_id
    TestExecutionResult.test_polarion_mapping[test_case_id] = item.nodeid


def _authentication():
    """Define if the authentication will be done by token or password.
    Used in ``pytest_terminal_summary`` hook"""
    if Credentials.POLARION_TOKEN == "":
        logger.info("Trying Polarion auth by Password")
        return "PASS_AUTH"
    else:
        logger.info("Trying Polarion auth by Token")
        return "TOKEN_AUTH"

# Assertion methods, messages, comments on Polarion Work Items

def polarion_assertion_selection_parametrize(results):
    """Function used on ``pytest_terminal_summary`` in case of 
    the test result being check is marked with parametrize. The 
    procedure add all the test cases outcome in a single string 
    using regex expressions to get the parameter and show the 
    outcome like:
    
    Test case FAILED
    [param0-param1] Passed
    [param2-param3] Failed
    ..."""
    import re

    all_results = []
    full_comment = "{}"
    line_comment_pat = "\n[{0}] {1}"

    for result in results:
        outcome = result.outcome == "passed"
        outcome_str = "Passed" if outcome else "Failed"
        all_results.append(outcome)

        pattern = r'\[(.*?)\]'
        text = result.nodeid
        matches = re.findall(pattern, text)

        full_comment = full_comment + line_comment_pat.format(
            matches[-1],
            outcome_str
        )

    full_comment = '<pre>' + full_comment + \
        '</pre><br>Comment from <strong>pytest-typhoon-polarion</strong> plugin'

    if np.all(all_results):
        message = "Test Case PASSED"
        comment = full_comment.format(message)
        record = Record.ResultType.PASSED    
    else:
        message = "Test Case FAILED"
        comment = full_comment.format(message)
        record = Record.ResultType.FAILED

    return message, comment, record


def test_case_failed_message_comment(longrepr):
    """Function used on ``polarion_assertion_selection``."""
    str_longrepr = str(longrepr)
    str_longrepr_sp = str_longrepr.split('\n')

    str_longrepr_mod = '\t' + str_longrepr.replace('\n', '\n\t')
    str_longrepr_html = (
        'Test Case <strong>FAILED</strong>:<br><pre>' + 
        str_longrepr_mod + 
        '</pre><br>Comment from <strong>pytest-typhoon-polarion</strong> plugin'
    )

    message = f"Test Case FAILED ({str_longrepr_sp[-1]})"
    comment = "" + str_longrepr_html + "<br><br>"

    return message, comment, Record.ResultType.FAILED


def test_case_passed_message_comment():
    """Function used on ``polarion_assertion_selection``."""

    message = "Test Case PASSED"
    comment = "Test Case <strong>PASSED</strong><br>Comment from pytest-typhoon-polarion plugin"

    return message, comment, Record.ResultType.PASSED


def polarion_assertion_selection(results):
    """Function used on ``pytest_terminal_summary`` in case of 
    the test result being check is not marked with parametrize."""
    result = results[0]
    if result.outcome == "passed":
        return test_case_passed_message_comment()
    elif result.outcome == "failed":
        return test_case_failed_message_comment(result.longrepr)
    else:
        return Record.ResultType.BLOCKED


def _validation_test_run():
    """Check the server before test execution.
    This is executed on ``pytest_collection_modifyitems``."""
    run = PolarionTestRunRefs.run

    for test_case_id in PolarionTestRunRefs.test_cases:
        if not run.hasTestCase(test_case_id):
            raise TestCaseNotFoundError(
                f'The Test Case ID "{test_case_id}" was not found for the Test Run "{run.id}".'
            )

        if Settings.POLARION_VERSION == "2304":
            if _test_type_select_from_test_case(test_case_id) != 'automated':
                raise TestCaseTypeError(
                    f'The Test Case ID "{test_case_id}" is not configured as "Automated Test".'
                )


def _test_type_select_from_test_case(test_case_id):
    """Part of ``_validation_test_run`` method that 
    executes on ``pytest_collection_modifyitems``."""
    project = PolarionTestRunRefs.project
    test_case = project.getWorkitem(test_case_id)

    return test_case.customFields['Custom'][0]['value']['id']


def _process_hyperlinks_from_polarion(test_case_links):
    """Get the Hyperlinks from a Work item.
    Used on ``pytest_terminal_summary``."""
    hyperlinks = []
    
    for hyperlink_item in test_case_links['Hyperlink']:
        hyperlinks.append(hyperlink_item['uri'])

    return hyperlinks


def _validate_boolean_option(option):
    if isinstance(option, bool):
        return option
    elif isinstance(option, str):
        if option.lower() == "true":
            return True
        elif option.lower() == "false":
            return False
        else:
            raise ConfigurationError(
                "Option used for POLARION_VERIFY_CERTIFICATE on secrets file is not valid!"
            ) from None
    else:
        pass
