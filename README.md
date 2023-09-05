# Pytest plugin for integration with Siemens Polarion
**Note:** Plugin under development

This plugin is part of [pytest framework]([url](https://docs.pytest.org/)) integration 
with Siemens Polarion developed by Typhoon HIL.

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
git clone https://github.com/typhoon-hil/pytest-typhoon-polarion.git
```

And use ``pip install`` command locally in the root of the project:
```console
pip install .
```

----

**Note:** 

The plugin was developed and executes with no problems on Python 3.9.6.
Other python version may require modifications or use of Polarion REST API. Since 
this plugin was developed on top of 
[a open-source Polarion project](https://pypi.org/project/polarion/).

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
--polarion-project-id=<Project_id> --polarion-test-run=<TestRun_id> 
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
My Account > Personal Access Token (upper-center, below the page header).

Also, by usage, is noticed that Polarion don`t allow request after a token or XML
key is configured, after configuring any stronger authentication method the password
is deprecated, even if this one is expired or deleted.

<!---

### Exception ``requests.exceptions.SSLError`` Reanalize this issue

The full name exception: 

```plain text
requests.exceptions.SSLError: HTTPSConnectionPool(host='localhost', port=80): 
Max retries exceeded with url: /polarion/ws/services 
(Caused by SSLError(SSLError(1, '[SSL: WRONG_VERSION_NUMBER] wrong version number 
(_ssl.c:1129)')))
```

Can happen when the **Polarion Server** and the **Apache** is not start correctly.
In case the tests results are not able to be uploaded to Polarion, please check if
Apache is running and the machine has none SSL Certificates issues with Polarion.

Also, by usage, is noticed that Polarion don`t allow request after a token or XML
key is configured, after configuring any stronger authentication method password
is deprecated, even if this one is expired or deleted.
-->
