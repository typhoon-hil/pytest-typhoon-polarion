from _pytest.terminal import TerminalReporter
import os
from pathlib import Path
from polarion.workitem import Workitem
from polarion.record import Record
from zeep.exceptions import Fault
import numpy as np

from ..runtime_settings import TestExecutionResult, Settings, PolarionTestRunRefs
from ..work_items_utils import get_uid_values, get_test_case_url
from ..exceptions import TestCaseTypeError

# process_pytest_results function

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


def process_pytest_results(terminalreporter: TerminalReporter):  # Reviewed and
    _fill_keys(terminalreporter.stats, 'passed')
    _fill_keys(terminalreporter.stats, 'failed')
    _fill_keys(terminalreporter.stats, 'skipped')


def get_uid_report_values():  # Reviewed
    full_alluredir = os.path.abspath(Settings.ALLUREDIR)
    html_path = Path(full_alluredir).parent / 'allure-html'

    uid_test_mapping, parent_uid = get_uid_values(html_path)
    
    TestExecutionResult.uid_test_mapping = uid_test_mapping
    TestExecutionResult.parent_uid = parent_uid


def _process_hyperlinks_from_polarion(test_case_links):
    """Get the Hyperlinks from a Work item.
    Used on ``pytest_terminal_summary`` -> 
    ``set_hyperlink_on_polarion_server``."""
    hyperlinks = []
    
    for hyperlink_item in test_case_links['Hyperlink']:
        hyperlinks.append(hyperlink_item['uri'])

    return hyperlinks


def set_hyperlink_on_polarion_server(test_case_id, test_results):
    project = PolarionTestRunRefs.project
    run = PolarionTestRunRefs.run

    test_case_record = run.getTestCase(test_case_id)
    test_case_item = project.getWorkitem(test_case_id)

    # - Remove all them and re-enter with Allure address
    test_node = test_results[0].nodeid
    test_case_links = test_case_item.hyperlinks

    # If hyperlink list is not empty it will be clean up
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



def __test_case_failed_message_comment(longrepr):
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


def __test_case_passed_message_comment():
    """Function used on ``polarion_assertion_selection``."""

    message = "Test Case PASSED"
    comment = "Test Case <strong>PASSED</strong><br>Comment from pytest-typhoon-polarion plugin"

    return message, comment, Record.ResultType.PASSED

# Assertion methods, messages, comments on Polarion Work Items

def _polarion_assertion_selection_parametrize(results):
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


def _polarion_assertion_selection(results):
    """Function used on ``pytest_terminal_summary`` in case of 
    the test result being check is not marked with parametrize."""
    result = results[0]
    if result.outcome == "passed":
        return __test_case_passed_message_comment()
    elif result.outcome == "failed":
        return __test_case_failed_message_comment(result.longrepr)
    else:
        return Record.ResultType.BLOCKED


def set_assertion_and_comments_on_polarion_server(test_case_id, test_results):
    project = PolarionTestRunRefs.project
    run = PolarionTestRunRefs.run

    test_case_record = run.getTestCase(test_case_id)
    test_case_item = project.getWorkitem(test_case_id)
    # TODO: Add parametrize and check how this works on XRAY Plugin
    if len(test_results) > 1:  # parametrize mark
        message, comment, polarion_result = _polarion_assertion_selection_parametrize(test_results)
    else:
        message, comment, polarion_result = _polarion_assertion_selection(test_results)

    # return message, comment, polarion_result

    if Settings.ALLOW_COMMENTS:
        if Settings.USER_COMMENTS is not None or Settings.USER_COMMENTS != '':
            user_comment = Settings.USER_COMMENTS.replace(r"\n", "<br>")
            comment = f"<strong>User Comment:</strong><br>{user_comment}<br><br>{comment}"
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
            The error "zeep.exceptions.Fault: com.polarion.core.util.exceptions.UserFriendlyRuntimeException: 
            Sorry this action cannot be executed without providing an e-signature in the Polarion portal: 
            Execution of a Test Case in the Test Run 'REL'."
            falls here when the Test Run is not configured as "Automated".
            """
            raise fault from None
