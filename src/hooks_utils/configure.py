import pytest
from polarion.polarion import Polarion
from ..runtime_settings import Settings, Credentials

from ..utils import read_or_get, read_or_get_ini
from ..exceptions import ConfigurationError, InvalidCredentialsError
from ..runtime_settings import PolarionTestRunRefs

from .logs import write_log


# set_init_files_config function

def _validate_boolean_option(option, opt_label):
    """Used to validate options on _validate_boolean_option function"""

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


def set_init_files_config(config: pytest.Config):  # Reviewed 
    Settings.ALLUREDIR = config.getoption('--alluredir')
    
    secrets = config.getoption('secrets')
    config_file = config.getoption('config_file')

    Credentials.POLARION_HOST = read_or_get(secrets, 'POLARION_HOST', '')
    Credentials.POLARION_USER = read_or_get(secrets, 'POLARION_USER', '')
    Credentials.POLARION_PASSWORD = read_or_get(secrets, 'POLARION_PASSWORD', '')
    Credentials.POLARION_TOKEN = read_or_get(secrets, 'POLARION_TOKEN', '')

    Settings.LOG_FILE_PATH = read_or_get_ini(config_file, 'LOG_FILE_PATH', config.getoption('log_plugin_report'), section="log_file")
    Settings.ENABLE_LOG_FILE = read_or_get_ini(config_file, 'ENABLE_LOG_FILE', False, section="log_file")

    Settings.POLARION_TEST_RUN = read_or_get_ini(config_file, 'POLARION_TEST_RUN', config.getoption('polarion_test_run'), section="polarion")
    Settings.POLARION_PROJECT_ID = read_or_get_ini(config_file, 'POLARION_PROJECT_ID', config.getoption('polarion_project_id'), section="polarion")
    Settings.POLARION_VERSION = read_or_get_ini(config_file, 'POLARION_VERSION', "2304", section="polarion")

    Settings.WEB_URL = read_or_get_ini(config_file, 'WEB_URL', config.getoption('web_url'), section='polarion') 
    Settings.ALLOW_COMMENTS = read_or_get_ini(config_file, 'ALLOW_COMMENTS', config.getoption('allow_comments'), section='polarion')
    
    Settings.ALLOW_COMMENTS = _validate_boolean_option(Settings.ALLOW_COMMENTS, "ALLOW_COMMENTS")
    
    Settings.POLARION_VERIFY_CERTIFICATE = read_or_get(secrets, 'POLARION_VERIFY_CERTIFICATE', "True")
    Settings.POLARION_VERIFY_CERTIFICATE = _validate_boolean_option(Settings.POLARION_VERIFY_CERTIFICATE, "POLARION_VERIFY_CERTIFICATE")
    
    Settings.USER_COMMENTS = read_or_get_ini(config_file, 'USER_COMMENTS', config.getoption('user_comments'), section="polarion")

# connect_polarion_server function
    
def _authentication():  # Reviewed and tested
    """Define if the authentication will be done by token or password.
    Used in ``pytest_terminal_summary`` hook"""
    if Credentials.POLARION_TOKEN == "":
        write_log("Trying Polarion auth by Password")
        return "PASS_AUTH"
    else:
        write_log("Trying Polarion auth by Token")
        return "TOKEN_AUTH"


def connect_polarion_server():  # Reviewed and tested
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

    # Add in a global class all the polarion test run references (1/2)
    PolarionTestRunRefs.client = client


# get_server_project_and_test_run function

def get_server_project_and_test_run():  # Reviewed and tested
    client = PolarionTestRunRefs.client
    
    # Add in a global class all the polarion test run references (2/2)
    project = client.getProject(Settings.POLARION_PROJECT_ID)
    run = project.getTestRun(Settings.POLARION_TEST_RUN)
    
    PolarionTestRunRefs.project = project
    PolarionTestRunRefs.run = run
