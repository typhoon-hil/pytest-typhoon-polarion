
polarion_test_cases = {}

class Settings:
    POLARION_HOST = ''
    POLARION_USER = ''
    POLARION_PASSWORD = ''
    # POLARION_TOKEN = ''
    POLARION_PROJECT_ID = ''
    POLARION_TEST_RUN = ''


class TestExecutionResult:
    polarion_test_mapping = {}  # test_name: polarion_test_id (str: str)

    result_polarion_mapping = {}  # polarion_test_id: test_results (str: list)
    test_polarion_mapping = {}  # Inverted polarion_test_mapping dict


class PolarionTestRunRefs:
    client = None
    project = None
    run = None
    test_cases = list()
