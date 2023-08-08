# Quick Demo with Polarion setup

## Installation (Windows)

Polarion requires license with free trial use without external requests,
only local ones.

After run the installation the server is automatically placed on
https://localhost:80. The user can search for Polarion on the initial menu and 
start the menu, open the main page, and other server related activities.

In the main screen the first login is user: ``admin`` and password: ``admin``. 
Tokens and other user can be created on the software as well teams and holes.

## Quick-Start

This quick-start will guide regarding how to create a project, Test Cases, and
Test Runs to be used byt the plugin.
The image show the main page of polarion:

![0_polarion_main_page.png](docs/images/0_polarion_main_page.png)

*Step 1/12*: In the upper bar you can create a new project clicking on ``Default Repository``, 
the one that will be used for this demo:

![1_create_new_project.png](docs/images/1_create_new_project.png)

*Step 2/12*: Select the project name (will be used as ID for ``pytest-typhoon-polarion`` 
plugin later by the option ```) and go **Next**:

![2_project_id.png](docs/images/2_project_id.png)

*Step 3/12*: For the Template select ``Agile Software Project (Product and Release Backlogs, 
Sprint Management, Quality Assurance, Builds)``. This project has configured the
issues as **Test Cases** and later can be used on the **Test Runs**:

![3_project_template.png](docs/images/3_project_template.png)

*Step 4/12*: Confirm with **Next**, and continue until the **Creation** stage and 
wait a few seconds. The project is created successfully. Now, navigate on the 
lateral tab on (1) **Work Items** then select the (2) "+" button, and (3) 
**Test Case**.

![4a_create_test_case.png](docs/images/4a_create_test_case.png)

*Step 5/12*: Fill the test specification **Title**, Test Type as Automated Test and click on 
the **Save** button, automatically Polarion will create an ID for the test case,
that will be used to mark the test later on pytest:

![4b_create_test_case.png](docs/images/4b_create_test_case.png)

*Step 6/12*: After that change the Status to ``Perform action Activate`` and **Save** once
again:

![4c_create_test_case.png](docs/images/4c_create_test_case.png)



*Step 7/12*: With the test or tests cases created select on the lateral menu **Expand** and 
then **Test Runs**:

![5a_create_test_runs.png](docs/images/5a_create_test_runs.png)

On Test Runs you can **Manage Templates** in the upper right corner. 
You can create a new Template or change the existent one in the list.
In order to work with pytest the template needs to be Type ``Automated``. 
In this example we replace the ``manual`` type to ``Automated`` in the Release
Test templates. When marked as automated the test ca still be run as manual.

![5a2_create_test_runs.png](docs/images/5a2_create_test_runs.png)

*Step 8/12*: Click in **New** and select a Template type and a Test Run ID, 
which will be also configured by the plugin, using the option 
``--polarion-test-run``.

![5b_create_test_runs.png](docs/images/5b_create_test_runs.png)

*Step 9/12*: After created configure the **Query** of the test run to collect
the test based on filter. In this example the filter selected is 
``type:testcase AND status:active``.

![5c_create_test_runs.png](docs/images/5c_create_test_runs.png)

*Step 10/12*: Automatically the Test Case created will be linked with the Test 
Run. Now, so the plugin can change the Test Results one manual execution needs 
to happen through Polarion. Click in **Execute Tests**.

![5d_create_test_runs.png](docs/images/5d_create_test_runs.png)

*Step 11/12*: Click to **Start** the test and give any **Veredict** 
(E.g.: Blocked). And save the Veredict.

![5e_create_test_runs.png](docs/images/5e_create_test_runs.png)

![5f_create_test_runs.png](docs/images/5f_create_test_runs.png)

The test case will shown as executed instead of waiting.

![5g_create_test_runs.png](docs/images/5g_create_test_runs.png)


*Step 12/12*: Now with the Test Run populated we can start to write our test 
using pytest. Create a file called ``test_demo_example.py`` and write the 
follow simple test.

```python
import pytest
from typhoon.test.signals import pandas_sine
import typhoon.test.harmonic as harmonic
    
@pytest.mark.polarion(test_id="DE-391")  # ID from the Polarion Test Case
def test_check_vab_freq():
    amp = 1
    freq = 60
    
    # Signal is an API generated signal, can also be capture from HIL Simulation
    signal = pandas_sine(amplitude=amp, frequency=freq, Ts=1e-3)

    # Frequency Analysis
    content = harmonic.frequency_content(signal, 240)

    assert abs(content(60)) == amp, "60 Hz amplitude not correct"
```

And add the secrets file in the same folder with your user information:
```plain text
POLARION_HOST=http://localhost:80/polarion
POLARION_USER=admin
POLARION_PASSWORD=admin
```

And execute using the following command (Typhoon-HIL Control Center needs to be 
installed):

```commandline
pytest .\test_demo_example.py --polarion-project-id=DemoExample --polarion-test-run=REL --secrets=secrets 
```

This test is a pass case and is possible to see on Polarion at the end of the
execution the test assertion changed. With this setup done is possible to write
more test cases in Polarion, implement using Typhoontest API and have all the
Test Results in Polarion page.

![5h_create_test_runs.png](docs/images/5h_create_test_runs.png)

## More about authentication

blank