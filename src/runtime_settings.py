
polarion_test_cases = {}


class Credentials:
    POLARION_HOST = ''
    POLARION_USER = ''
    POLARION_PASSWORD = ''
    POLARION_TOKEN = ''


class Settings:
    POLARION_PROJECT_ID = ''
    POLARION_TEST_RUN = ''
    WEB_URL = ''
    ALLUREDIR = ''
    ALLOW_COMMENTS = None
    POLARION_VERIFY_CERTIFICATE = True
    POLARION_VERSION = '2304'

    LOG_PATH = ''
    ENABLE_LOG_FILE = False
    USER_COMMENTS = ''


class TestExecutionResult:
    polarion_test_mapping = {}  # test_name: polarion_test_id (str: str)

    result_polarion_mapping = {}  # polarion_test_id: test_results (str: list)
    test_polarion_mapping = {}  # Inverted polarion_test_mapping dict

    uid_test_mapping = {}  # test_name: uid (str: str)
    parent_uid = None


class PolarionTestRunRefs:
    client = None
    project = None
    run = None
    test_cases = list()
