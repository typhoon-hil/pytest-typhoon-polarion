from ..runtime_settings import Settings, Credentials


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


def logging_get_options(config):
    write_log("pytest_configure", section=True, sub=False, type='w')
    write_log("Getting options:")
    write_log(f"* POLARION_TEST_RUN: {repr(config.getoption('polarion_test_run'))}")
    write_log(f"* POLARION_PROJECT_ID: {repr(config.getoption('polarion_project_id'))}")
    write_log(f"* WEB_URL: {repr(config.getoption('web_url'))}")
    write_log(f"* ALLOW_COMMENTS: {repr(config.getoption('allow_comments'))}\n")
    write_log(f"* secrets file: {repr(config.getoption('secrets'))}")
    write_log(f"* config_file file: {repr(config.getoption('config_file'))}\n")


def logging_secret_file_config():
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
    write_log(f"* Settings.USER_COMMENTS: {Settings.USER_COMMENTS} ({type(Settings.USER_COMMENTS)})")


