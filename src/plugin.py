
POLARION_HOST = 'localhost:80'

POLARION_PROJECT_ID = 'admin'

XRAY_PLAN_KEY = ''
XRAY_FAIL_SILENTLY = False
XRAY_TOKEN = ''
JIRA_HOST = ''
JIRA_USER = ''
JIRA_PASSWORD = ''
JIRA_AUTH = []
RUN_CONFIG = ''
ALLURE_URL = ''

def pytest_configure(config):
    config.addinivalue_line('markers',
                            'polarion(test_id): ID register on Polarion for the test case available on the Test Run')



