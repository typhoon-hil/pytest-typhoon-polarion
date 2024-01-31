import os

from ..exceptions import TestCaseTypeError, TestCaseNotFoundError
from ..runtime_settings import (
    TestExecutionResult,
    Settings,
    PolarionTestRunRefs
)

def _get_polarion_marker(item):
    """Catches the polarion marker.
    Used in ``_store_item`` function > ``pytest_collection_modifyitems`` hook"""
    return item.get_closest_marker('polarion')


def store_item(item):
    """On colletion storage the tests node and the polarion tags.
    Used in ``pytest_collection_modifyitems`` hook"""

    marker = _get_polarion_marker(item)

    if not marker:
        return

    test_case_id = marker.kwargs['test_id']
    PolarionTestRunRefs.test_cases.append(test_case_id)
    TestExecutionResult.polarion_test_mapping[item.nodeid] = test_case_id
    TestExecutionResult.test_polarion_mapping[test_case_id] = item.nodeid


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


def _test_type_select_from_test_case(test_case_id):
    """Part of ``_validation_test_run`` method that 
    executes on ``pytest_collection_modifyitems``."""
    project = PolarionTestRunRefs.project
    test_case = project.getWorkitem(test_case_id)
    return test_case.customFields['Custom'][0]['value']['id']


def validation_test_run():
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
