import pytest
from _pytest.terminal import TerminalReporter
import os

import logging

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

from .hooks_utils.logs import write_log
from .hooks_utils import logs as _logs

from .hooks_utils import configure as _configure
from .hooks_utils import terminal_summary as _term_summ

logger = logging.getLogger(__file__)


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
    group.addoption(
        '--log-plugin-report-path',
        dest='log_plugin_report',
        help='Allow a log file to be created on the path pass through this option'
    )
    group.addoption(
        '--user-comments',
        dest='user_comments',
        help='Allow a log file to be created on the path pass through this option'
    )


def pytest_configure(config: pytest.Config):
    config.addinivalue_line(
        'markers',
        'polarion(test_id): ID register on Polarion for the test case available on the Test Run')
        
    _logs.logging_get_options(config)

    secrets = config.getoption('secrets')

    if secrets is None:
        raise ConfigurationError(
            '"secrets" files used by pytest-typhoon-polarion was not configured.\n'
            'In case the plugin is not needed uninstall the package using:\n'
            '\t"pip uninstall pytest-typhoon-polarion -y"')

    _configure.set_init_files_config(config)

    _logs.logging_secret_file_config()

    _configure.connect_polarion_server()

    _configure.get_server_project_and_test_run()


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


def pytest_terminal_summary(terminalreporter: TerminalReporter):
    _term_summ.process_pytest_results(terminalreporter)

    if Settings.WEB_URL is not None:
        _term_summ.get_uid_report_values()

    for test_case_id, test_results in TestExecutionResult.result_polarion_mapping.items():
        # Hyperlink on Test Case - Work Items 
        # Added if web-url is not NoneType
        if Settings.WEB_URL is not None:
            _term_summ.set_hyperlink_on_polarion_server(test_case_id, test_results)       
        _term_summ.set_assertion_and_comments_on_polarion_server(test_case_id, test_results)


def pytest_sessionfinish(session):
    pass


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
        else:
            try:  # TODO: Remove this in the future
                if Settings.ENABLE_LOG_FILE:
                    _store_test_case(test_case_id)
            except:
                pass


def _test_type_select_from_test_case(test_case_id):
    """Part of ``_validation_test_run`` method that 
    executes on ``pytest_collection_modifyitems``."""
    project = PolarionTestRunRefs.project
    test_case = project.getWorkitem(test_case_id)
    return test_case.customFields['Custom'][0]['value']['id']


def _store_test_case(test_case_id):
    """Part of ``_validation_test_run`` method that 
    executes on ``pytest_collection_modifyitems``."""
    project = PolarionTestRunRefs.project
    test_case = project.getWorkitem(test_case_id)
    
    from pathlib import Path
    if Settings.LOG_PATH is None:
        dir_path = Path().resolve()
    else:
        dir_path = Path(Settings.LOG_PATH).resolve()
    
    dir_path_full = dir_path / "logs"
    if not dir_path_full.exists():
        os.mkdir(dir_path_full)

    with open(dir_path_full / "test_case_example.txt", 'w') as ftxt:
        ftxt.write(repr(test_case.customFields))
