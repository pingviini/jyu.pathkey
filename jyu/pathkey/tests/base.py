"""Test setup for integration and functional tests.
 
When we import PloneTestCase and then call setupPloneSite(), all of
Plone's products are loaded, and a Plone site will be created. This
happens at module level, which makes it faster to run each test, but
slows down test runner startup.
""" 

from Products.Five import zcml 
from Products.Five import fiveconfigure 

from Testing import ZopeTestCase as ztc 

from Products.PloneTestCase import PloneTestCase as ptc 
from Products.PloneTestCase.layer import onsetup 


@onsetup 
def setup_product(): 
    """Set up the package and its dependencies.
    
    The @onsetup decorator causes the execution of this body to be
    deferred until the setup of the Plone site testing layer. We could
    have created our own layer, but this is the easiest way for Plone
    integration tests.
    """ 
    
    # Load the ZCML configuration for the example.tests package.
    # This can of course use <include /> to include other packages.
   
    fiveconfigure.debug_mode = True 
    import jyu.pathkey 
    zcml.load_config('configure.zcml', jyu.pathkey) 
    fiveconfigure.debug_mode = False 
    ztc.installPackage('jyu.pathkey')
    
setup_product() 
ptc.setupPloneSite(products=['jyu.pathkey']) 

from Products.CMFCore.utils import getToolByName

class TestCase(ptc.PloneTestCase):
    """We use this base class for all the tests in this package. If
    necessary, we can put common utility or setup code in here. This
    applies to unit test cases.
    """


class FunctionalTestCase(ptc.FunctionalTestCase):
    """We use this class for functional integration tests that use
    doctest syntax. Again, we can put basic common utility or setup
    code in here.
    """

    def afterSetUp(self):       
        self.portal.error_log._ignored_exceptions = ()
        self.portal.portal_membership.addMember('contributor', 'secret',
                                                ('Member', 'Contributor'), [])
        self.portal.portal_membership.addMember('reviewer', 'secret',
                                                ('Member', 'Contributor', 'Editor', 'Reviewer'), [])
        

