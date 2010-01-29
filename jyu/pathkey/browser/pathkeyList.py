from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from jyu.pathkey.interfaces import IPathkey

class PathkeyListView(BrowserView):
    """ Pathkey Listing """

    __call__ = ViewPageTemplateFile('pathkeylist_view.pt')

    def __init__(self, context, request):
        """ set up a few convenience object attributes """

        self.context = context
        self.request = request
        self.pc = getToolByName(self.context, 'portal_catalog')
        self.mt = getToolByName(self.context, 'portal_membership')

    def searchPathkeyItems(self):
        user = self.mt.getAuthenticatedMember().getUserName()
        results = self.pc.searchResults(object_provides='jyu.pathkey.interfaces.IPathkey', owner = user)

        return results