*** Settings ***

Resource  plone/app/robotframework/selenium.robot
Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open test browser
Test Teardown  Close all browsers

*** Test Cases ***

Site Administrator can set pathkey
    I'm logged in as a 'Site Administrator'
    Go to  ${PLONE_URL}/published-folder
    I open the actions menu
    Click link  plone-contentmenu-actions-pathkey
    Page should contain  Warning
    Page should contain  You are trying to adjust pathkey for a containers default view
    Page should not contain Textfield  form.path_key
    Page should not contain Textfield  form.pathkey_owner
    Page should not contain Textfield  form.pathkey_owner_email
    Click link  parent-pathkey-form-link
    Page should contain Textfield  form.path_key
    Page should contain Textfield  form.pathkey_owner
    Page should contain Textfield  form.pathkey_owner_email
    Input text  form.path_key  1111
    Input text  form.pathkey_owner  Example User
    Input text  form.pathkey_owner_email  example@example.com
    Click button  form.actions.send
    Page should contain  Added a new pathkey and related information about pathkey owner.
    Page should contain  Access restricted by contents owner. Please give correct pathkey to continue.
    Page should contain  Enter the pathkey
    Page should contain Element  form.pathkey
    Page should contain  Pathkey owner: Example User
    Page should contain  You can ask the correct pathkey by sending email to
    Page should contain  Because you have permissions to modify content you can see the pathkey which is:

User can access pathkey protected content
    Given Manager has added pathkey
    Go to  ${PLONE_URL}/published-folder
    Page should contain  Access restricted by contents owner. Please give correct pathkey to continue.
    Page should contain  Enter the pathkey
    Input text  form.pathkey  1111
    Click button  form.actions.send
    Page should contain  Page 1

Pathkey is being asked if user tries to get content with direct link
    Given Manager has added pathkey
    Go to  ${PLONE_URL}/published-folder/page-1
    Page should contain  Access restricted by contents owner. Please give correct pathkey to continue.
    Page should contain  Enter the pathkey
    Input text  form.pathkey  1111
    Click button  form.actions.send
    Page should contain  Page 1

*** Keywords ***

I open the actions menu
    Click Element  id=plone-contentmenu-actions
    Page should contain  Pathkey

I'm logged in as a '${ROLE}'
    Enable autologin as  ${ROLE}
    Go to  ${PLONE_URL}

Manager has added pathkey
    I'm logged in as a 'Site Administrator'
    Go to  ${PLONE_URL}/published-folder/pathkey-form
    Input text  form.path_key  1111
    Input text  form.pathkey_owner  Example User
    Input text  form.pathkey_owner_email  example@example.com
    Click button  form.actions.send
    Page should contain  Added a new pathkey and related information about pathkey owner.
    Disable autologin
