import pytest
from _pytest.terminal import TerminalReporter

from .runtime_settings import TestExecutionResult, Settings
from .exceptions import ConfigurationError
from .hooks_utils import logs as _logs
from .hooks_utils import configure as _configure
from .hooks_utils import terminal_summary as _term_summ
from .hooks_utils import collection_modifyitems as _coll_modi

import logging

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


def pytest_collection_modifyitems(config: pytest.Config, items: list[pytest.Item]):
    '''On this hook the Polarion Test ID markers is collected and organized in dictionaries. Also, 
    part of validation is made in order to not wait the whole test execution to discover that the 
    test results cannot be uploaded'''
    for item in items:
        _coll_modi.store_item(item)

    _logs.logging_test_cases_collected()
    _coll_modi.validation_test_run()


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
