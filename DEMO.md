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

![img.png](docs/images/0_polarion_main_page.png)

*Step 1/20*: In the upper bar you can create a new project clicking on ``Default Repository``, 
the one that will be used for this demo:

![img.png](docs/images/1_create_new_project.png)

*Step 2/20*: Select the project name (will be used as ID for ``pytest-typhoon-polarion`` 
plugin later by the option ```) and go **Next**:

![img_1.png](docs/images/2_project_id.png)

*Step 3/20*: For the Template select ``Agile Software Project (Product and Release Backlogs, 
Sprint Management, Quality Assurance, Builds)``. This project has configured the
issues as **Test Cases** and later can be used on the **Test Runs**:

![img_2.png](docs/images/3_project_template.png)

*Step 4/20*: Confirm with **Next**, and continue until the **Creation** stage and 
wait a few seconds. The project is created successfully. Now, navigate on the 
lateral tab on (1) **Work Items** then select the (2) "+" button, and (3) 
**Test Case**.

![img.png](docs/images/4a_create_test_case.png)

*Step 5/20*: Fill the test specification **Title**, Test Type as Automated Test and click on 
the **Save** button:

![img_1.png](docs/images/4b_create_test_case.png)

*Step 6/20*: After that change the Status to ``Perform action Activate`` and **Save** once
again:

![img_2.png](docs/images/4c_create_test_case.png)

*Step 7/20*: With the test or tests cases created select on the lateral menu **Expand** and 
then **Test Runs**:

![img_3.png](docs/images/5a_create_test_runs.png)

*Step 8/20*: Click in **New** and select a Template type and a Test Run ID, which will be al

![img_4.png](docs/images/5b_create_test_runs.png)

*Step 9/20*: 