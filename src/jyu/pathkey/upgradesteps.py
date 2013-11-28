
from Products.CMFCore.utils import getToolByName

def upgrade1to2(context):
    setup_tool = getToolByName(context, 'portal_setup')
    setup_tool.runAllImportStepsFromProfile('profile-jyu.pathkey:upgrade1to2')



