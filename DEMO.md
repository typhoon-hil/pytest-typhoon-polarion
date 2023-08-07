# Quick Demo with Polarion setup

## Installation (Windows)

Polarion requires license with free trial use without external requests,
only local ones.

After run the installation the server is automatically placed on
https://localhost:80. The user can search for Polarion on the initial menu and 
start the menu, open the main page, and other server related activities.

In the main screen the first login is user: ``admin`` and password: ``admin``. 
Tokens and other user can be created on the software as well teams and holes.

The image show the main page of polarion:

![img.png](docs/images/0_polarion_main_page.png)

In the upper bar you can create a new project clicking on ``Default Repository``, 
the one that will be used for this demo:

![img.png](docs/images/1_create_new_project.png)

Select the project name (will be used as ID for ``pytest-typhoon-polarion`` 
plugin later) and go **Next**:

![img_1.png](docs/images/2_project_id.png)

For the Template select ``Agile Software Project (Product and Release Backlogs, 
Sprint Management, Quality Assurance, Builds)``. This project has configured the
issues as **Test Cases** and later can be used on the **Test Runs**:

![img_2.png](docs/images/3_project_template.png)

Confirm with **Next**, and continue until the **Creation** stage and wait a 
few seconds. The project is created sucessfully.

