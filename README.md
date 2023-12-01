
![PyPI - Version](https://img.shields.io/pypi/v/pytest-typhoon-polarion.svg) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pytest-typhoon-polarion)

## Pytest plugin for integration with Siemens Polarion

This plugin is part of [pytest framework](https://docs.pytest.org/) integration with Siemens Polarion developed by Typhoon HIL. Developed on top of [an open-source Polarion project](https://pypi.org/project/polarion/). **Developed using Siemens Polarion ALM 2304 version**.

On Polarion struct the template used was ``Agile Software Project (Product and Release Backlogs, Sprint Management, Quality Assurance, Builds)``. On this template is possible to write ``Test Cases`` and also to create ``Test Runs`` with the tests case selected.

In order to make work, in this version of the plugin, the user needs to describe the test cases and connect then with the ``Test Runs``, run the tests once and then the plugin will be able using the secrets file and the options to sync the test result with Polarion Test Runs.

### More Features
- Marker ``@pytest.mark.polarion`` created to link Polarion Test Case with the Pytest prodedure.
- When ``@pytest.mark.parametrize`` are used all the test cases can be shown on Work Items comments.
- Hyperlink to the Allure Report on the Work Items page.

### Requirements
- typhoontest>=1.27.0
- polarion==1.3.0

## Installation

You can create a new environment or install on system Python directly from PyPI, using:
```properties
pip install pytest-typhoon-polarion
```

Or cloning the repository using the follow commands:
```properties
git clone https://github.com/typhoon-hil/pytest-typhoon-polarion.git
```

And use ``pip install`` command locally in the root of the project:
```properties
pip install .
```

----
## Getting Started

Get your credentials and filled the ``secrets`` file:

```ini
POLARION_HOST=<Polarion-Host-Location>  # If is on localhost then ``http://localhost:80/polarion``
POLARION_USER=<Username>
POLARION_PASSWORD=<password>  # Is not needed if you have the Token
POLARION_TOKEN=<Personal-Access-Token>
POLARION_VERIFY_CERTIFICATE=False  # In case of HTTPS is used, SSL Error may happen and this option needs to be set as 'False'
```

More recently, from version 1.0.2 is possible to configure a ``config.ini`` file and set information regarding the project and plugin functionalities:
```ini
[polarion]
POLARION_PROJECT_ID=TestDev
POLARION_TEST_RUN=REL-001
ALLOW_COMMENTS=True
WEB_URL=http://localhost:8000/allure-html/
POLARION_VERSION=2304
# POLARION_VERSION="22 R2"

[log_file]
ENABLE_LOG_FILE=True
LOG_FILE_PATH=C:\Users\user\Desktop
```

Further on this document is shown the options available and how to configure ([List of options available](#options_table))

Now, the **Project ID** used when created and the **Test Run ID** needs to be passed to the options, like:

```properties
pytest <tests_folder> --secrets=secrets --polarion-project-id=<Project_id> --polarion-test-run=<TestRun_id> 
```

And the test cases needs to be link with the pytest test implemented, for each test case you need one pytest test, if the Test ID is not used to sync with Polarion that test case will be ignored:

```python
import pytest

@pytest.mark.polarion(test_id="<test_case_id>")
def test_check_signal_Vab_freq():
    ...
    assert True
```

More details and a Demo of the plugin can be found on the [Github Page](https://github.com/typhoon-hil/pytest-typhoon-polarion/blob/master/demo/DEMO.md).

### More options available

Using the Work Items comments and hyperlinks can be added on Polarion the address for the Allure report and the outcome result with the assertion message.

Using the option `--web-url` you can point to the Allure Report placeholder, when running Jenkins or locally serve, and the link in the Work Item result will be added to the report. For example:

```properties
typhoon-python -m pytest ... --web-url=http://localhost:8000/allure-html/
```

And in order to add extra information about the test outcome, or when the test has several test cases, using the `@pytest.mark.parametrize` the option `--allow-comments` can be also used:

```properties
typhoon-python -m pytest ... --allow-comments
```

In order to inform the ``config.ini`` file the option ``--config`` is add to the plugin:

```properties
typhoon-python -m pytest ... --config=config.ini
```

### <a name="options_table"></a> List of options available

Here follows a list of options available through the new ``config.ini`` file and also as options, from the previous versions:

| Parameter               | ``config.ini`` file                       | ``config.ini`` section | Command-line options                          |
|-------------------------|-------------------------------------------|------------------------|-----------------------------------------------|
| Secrets file path       | (*) Only command-line                     | -                      | --secrets                                     |
| Configuration file path | Only command-line                         | -                      | --config                                      |
| Polarion Project ID     | POLARION_PROJECT_ID=TestDev               | [polarion]             | --polarion-project-id=TestDev                 |
| Polarion Test Run ID    | POLARION_TEST_RUN=REL-001                 | [polarion]             | --polarion-test-run=REL-001                   |
| Comments by the plugin  | ALLOW_COMMENTS=True                       | [polarion]             | --allow-comments                              |
| Allure URL              | WEB_URL=http://localhost:8000/allure-html | [polarion]             | --web-url=http://localhost:8000/allure-html/  |
| Polarion Version        | POLARION_VERSION=22 R2                    | [polarion]             | Only through ``config.ini`` file              |
| Enable Log File         | ENABLE_LOG_FILE=True                      | [log_file]             | Only through ``config.ini`` file              |
| Log File Path           | LOG_FILE_PATH=C:\Users\user\Desktop       | [log_file]             | --log-plugin-report-path=C:\User\user\Desktop |

(*) This option is mandatory.

**Description:**

* **Secrets file path**: Path to the files with the user/agent credentials.
* **Configuration file path**: Path to the files with the Polarion and plugin configuration.
* **Polarion Project ID**: ID of the project to be sync on Polarion Server.
* **Polarion Test Run ID**: ID for the Test Run of project configured in the previous option.
* **Comments by the plugin**: Comments that contains the assertion data for each Test Case/Work Item.
* **Allure URL**: The address that points to the Allure report used in the hyperlinks of each Test Case/Work Item.
* **Polarion Version**: Informs the plugin which Polarion Server version is being used.
* **Enable Log File**: Internal log_file with information regarding configuration (**Warning:** The token info is also logged, be careful to share this data).
* **Log File Path**: Path to save the log file. If not inform will be used the same as the one running the tests.

## Miscellaneous
### How to create a token
Show Settings (Engine below the Pn symbol in the left-up corner) > My Account > Personal Access Token (upper-center, below the page header).

Also, by usage, is noticed that Polarion don`t allow request after a token or XML key is configured, after configuring any stronger authentication method the password is deprecated, even if this one is expired or deleted.
