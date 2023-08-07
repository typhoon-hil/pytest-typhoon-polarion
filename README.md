# Pytest plugin for integration with Siemens Polarion

On Polarion struct the template used was ``Agile Software Project (Product and 
Release Backlogs, Sprint Management, Quality Assurance, Builds)``. On this 
template is possible to write ``Test Cases`` and also to create ``Test Runs`` 
with the tests case selected.

In order to make work, in this version of the plugin, the user needs to describe
the test cases and connect then with the ``Test Runs``, run the tests once 
and then the plugin will be able using the secrets file and the options to 
sync the test result with Polarion Test Runs.

## Installation

To install ``pytest-typhoon-polarion`` plugin creates a new Python  environment 
or install on system one cloning the project:
```console
git clone https://gitlab.typhoon-hil.com/dev/qa/pytest-polarion.git
```

And use ``pip install`` command locally in the root of the project:
```console
pip install .
```

----

**Note:** The plugin was developed and executes with no problems on Python 3.9.6.
Other python version may require modifications or use of Polarion REST API. Since 
this plugin was developed on top of 
[a open-source Polarion project](https://pypi.org/project/polarion/).

----

## Getting Started

Get your credentials and filled the secrets file:

```plain text
POLARION_HOST=<Polarion-Host-Location>  # If is on localhost then ``http://localhost:80/polarion``
POLARION_USER=<Username>
POLARION_PASSWORD=<password>  # Is not needed if you have the Token
POLARION_TOKEN=<Personal-Access-Token>
```

Now, the **Project ID** used when created and the **Test Run ID** needs to be
passed to the options, like:

```commandline
--polarion-test-run=<TestRun_id> --polarion-project-id=<Project_id>
```

And the test cases needs to be link with the pytest test implemented, for each
test case you need one pytest test, if the Test ID is not used to sync with
Polarion that test case will be ignored:

```python
import pytest

@pytest.mark.polarion(test_id="<test_case_id>")
def test_check_signal_Vab_freq():
    ...
    assert True
```


## Miscellaneous
### How to create a token (Valid for maximum 90 days):
Show Settings (Engine below the Pn symbol in the left-up corner) > 
My Account > Personal Access Token (upper-center, below the page header)