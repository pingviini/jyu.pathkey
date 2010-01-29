jyu.pathkey
===========

jyu.pathkey works by hooking event listener to AfterTravereEvent and checking if our final object or its parents have pathkey set.
To test this first we need to create folder structure.

Logging in to the site
----------------------

    >>> from Products.Five.testbrowser import Browser
    >>> browser = Browser()
    >>> portal_url = self.portal.absolute_url()
    >>> self.setRoles(('Manager',))
    >>> from Products.PloneTestCase import PloneTestCase as ptc
    >>> browser.open('http://nohost/plone/login_form')
    >>> browser.getControl(name='__ac_name').value = ptc.default_user
    >>> browser.getControl(name='__ac_password').value = ptc.default_password
    >>> browser.getControl('Log in').click()
    >>> 'You are now logged in' in browser.contents
    True


Add folder structure and some content in it
-------------------------------------------

    >>> browser.open(portal_url)
    >>> browser.getLink(id='folder').click()
    >>> browser.getControl(name='title').value = "Folder 1"
    >>> browser.getControl(name='form.button.save').click()
    >>> 'folder-1' in self.portal.objectIds()
    True

We need to publish our folders as there's no point testing pathkey
in a folder where users won't get in anyways.

    >>> browser.getLink('Advanced...').click()
    >>> browser.getControl(name='workflow_action').getControl(value='publish').selected = True
    >>> browser.getControl('Save').click()
    >>> browser.contents
    '...status...published...'
        
Let's add one sub-folder and publish it too

    >>> browser.getLink(id='folder').click()
    >>> browser.getControl(name='title').value = "Folder 2"
    >>> browser.getControl(name='form.button.save').click()
    >>> 'folder-2' in self.portal['folder-1'].objectIds()
    True
    >>> browser.getLink('Advanced...').click()
    >>> browser.getControl(name='workflow_action').getControl(value='publish').selected = True
    >>> browser.getControl('Save').click()
    >>> browser.contents
    '...status...published...'


Setting up the pathkey
----------------------

We go back to our first folder and set our pathkey to there.

    >>> browser.open(portal_url + '/folder-1')
    >>> browser.getLink('Add pathkey').click()
    >>> browser.contents
    '...If you want to protect contents of this folder, set a pathkey...'
    >>> browser.getControl(name='form.path_key').value = "1234"
    >>> browser.getControl(name='form.actions.send').click()
    
Now our pathkey is set and we should immediately have form which asks for a pathkey

    >>> browser.contents
    '...Access restricted by contents owner. Please give correct pathkey to continue...'


Wrong pathkey
-------------

Now that we have pathkey-requester form asking for a pathkey, 
let's try to give wrong pathkey first.

    >>> browser.getControl(name="form.pathkey").value="1245"
    >>> browser.getControl(name="form.actions.send").click()
    >>> browser.contents
    '...Access restricted by contents owner. Please give correct pathkey to continue...'   

It asks a correct pathkey.. hmm.. let's try to sneak past it to sub-folder.

    >>> browser.open(portal_url + '/folder-1/folder-2')
    >>> browser.contents
    '...Access restricted by contents owner. Please give correct pathkey to continue...'

Marvelous! We don't like people sneaking around. 


Correct pathkey
---------------

Now let's give pathkey-requester form the correct pathkey and see what happens.

    >>> browser.getControl(name="form.pathkey").value="1234"
    >>> browser.getControl(name="form.actions.send").click()
    >>> "Access restricted by contents owner" not in browser.contents
    True

We're in :)