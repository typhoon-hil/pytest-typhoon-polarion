
![PyPI - Version](https://img.shields.io/pypi/v/pytest-typhoon-polarion.svg) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pytest-typhoon-polarion)

## Pytest plugin for integration with Siemens Polarion

This plugin is part of [pytest framework](https://docs.pytest.org/) integration with Siemens Polarion developed by Typhoon HIL. Developed on top of [an open-source Polarion project](https://pypi.org/project/polarion/).

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

Get your credentials and filled the secrets file:

```ini
POLARION_HOST=<Polarion-Host-Location>  # If is on localhost then ``http://localhost:80/polarion``
POLARION_USER=<Username>
POLARION_PASSWORD=<password>  # Is not needed if you have the Token
POLARION_TOKEN=<Personal-Access-Token>
```

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

## Miscellaneous
### How to create a token
Show Settings (Engine below the Pn symbol in the left-up corner) > My Account > Personal Access Token (upper-center, below the page header).

Also, by usage, is noticed that Polarion don`t allow request after a token or XML key is configured, after configuring any stronger authentication method the password is deprecated, even if this one is expired or deleted.
