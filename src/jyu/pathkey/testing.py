from plone import api
from plone.app.testing import (
    applyProfile,
    FunctionalTesting,
    IntegrationTesting,
    PLONE_FIXTURE,
    PloneSandboxLayer,
    setRoles,
    TEST_USER_ID,
)
from plone.app.robotframework.testing import AUTOLOGIN_LIBRARY_FIXTURE
from plone.testing import z2

from zope.configuration import xmlconfig


class PathkeyTests(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import jyu.pathkey
        xmlconfig.file('configure.zcml', jyu.pathkey,
                       context=configurationContext)
        z2.installProduct(app, 'jyu.pathkey')

    def setUpPloneSite(self, portal):
        portal.portal_workflow.setDefaultChain("simple_publication_workflow")
        applyProfile(portal, 'jyu.pathkey:default')
        self.create_initial_content(portal)

    def create_initial_content(self, portal):
        """Creates initial folder structure for testing."""
        setRoles(portal, TEST_USER_ID, ['Manager'])

        published = api.content.create(type="Folder",
                                       title="Published folder",
                                       container=portal)

        subfolder = api.content.create(type="Folder",
                                       title="Subfolder 1",
                                       container=published)

        publishedpage = api.content.create(type="Document",
                                           title="Page 1",
                                           container=published)

        api.content.create(type="Document",
                           title="Page 2",
                           container=subfolder)

        api.content.transition(obj=published, transition="publish")
        api.content.transition(obj=publishedpage, transition="publish")

        published.manage_addProperty('default_page', type="text",
                                     value="page-1")


PATHKEY_FIXTURE = PathkeyTests()
PATHKEY_INTEGRATION_TESTING = IntegrationTesting(
    bases=(PATHKEY_FIXTURE,), name="PathkeyTests:Integration")
PATHKEY_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(PATHKEY_FIXTURE,), name="PathkeyTests:Functional")


PATHKEY_ROBOT_TESTING = FunctionalTesting(
    bases=(AUTOLOGIN_LIBRARY_FIXTURE, PATHKEY_FIXTURE, z2.ZSERVER_FIXTURE),
    name="PathkeyFunctional:Robot")
