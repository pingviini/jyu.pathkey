# -*- coding: utf-8 -*-

from Products.Five.formlib.formbase import PageForm
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.statusmessages.interfaces import IStatusMessage
from zope.formlib import form
from zope.interface import Interface
from zope.interface import alsoProvides, noLongerProvides
from zope.schema import Password, TextLine
from zope.component import getUtility

from jyu.pathkey.functions import getMD5SUM
from jyu.pathkey.interfaces import IPathkey
from jyu.pathkey.interfaces import IPathkeyControlPanelForm
from jyu.pathkey import _


class IPathkeyForm(Interface):
    """
    A pathkey schema
    """
    
    path_key = Password(title=_(u'Pathkey'),
                       description=_(u'If you want to protect contents of this folder, set a pathkey.'),
                       required=False)

class PathkeyForm(PageForm):
    """
    Pathkey form
    """
    template = ViewPageTemplateFile('set_pathkey.pt')
    form_fields = form.Fields(IPathkeyForm)
        
    def __init__(self, context, request):
        """ set up a few convenience object attributes """
        
        self.context, self.request = context, request
        self.response =  self.request.RESPONSE

   
    # Below we process the form with action_send form handler. 
    # First we check if there is already an existing path key 
    # and if there is we'll set a new path key. If path_key 
    # property doesn't exist in context we'll create it.
        
    @form.action("send")
    def action_send(self, action, data):
        
        status = IStatusMessage(self.request)
        new_path_key = data['path_key']
        
        if self.context.hasProperty('path_key'):
            old_path_key = self.context.get('path_key', None)
            if old_path_key and not new_path_key:
                self.context.manage_delProperties(['path_key'])
                noLongerProvides(self.context, IPathkey)
                status.addStatusMessage(_("Succesfully deleted the pathkey."))
            elif new_path_key:
                self.context.manage_changeProperties({'path_key': new_path_key})
                status.addStatusMessage(_("Modification of the pathkey succeeded."))
        else:
            if new_path_key:
                self.context.manage_addProperty('path_key', new_path_key, 'string')
                alsoProvides(self.context, IPathkey)
                status.addStatusMessage(_("Added a new pathkey."))
        
        self.context.reindexObject(idxs=['object_provides'])
        self.response.redirect(self.context.absolute_url())

        return ''

class IPathkeyCheck(Interface):
    """Pathkey requester interface"""

    pathkey = Password(
            title=_(u"Pathkey"),
            required=True)


class PathkeyRequest(PageForm):
    """Pathkey requester view"""

    template = ViewPageTemplateFile('pathkey_requester.pt')
    form_fields = form.Fields(IPathkeyCheck)
    
    def __init__(self, context, request):
        """ set up a few convenience object attributes """

        self.context = context
        self.request = request
        self.response = self.request.RESPONSE
        self.settings = self.context.portal_pathkey #IPathkeyControlPanelForm(self.context)
        self.language = self.request.get('LANGUAGE', 'fi')

    def getPathkeyTitle(self):
        if self.language == 'fi':
            return self.settings.pathkeyTitle_fi
        else:
            return self.settings.pathkeyTitle_en

    def getPathkeyDescription(self):
        if self.language == 'fi':
            return self.settings.pathkeyDescription_fi
        else:
            return self.settings.pathkeyDescription_en
    
    @form.action("send")
    def action_send(self, action, data):

#        status = IStatusMessage(self.request)
        try:
            suggested_pathkey = data['pathkey']
        except KeyError:
            suggested_pathkey = False
        
        if suggested_pathkey:
            pathkey = getMD5SUM(suggested_pathkey)
            self.response.setCookie('path_key', pathkey, path='/')

        self.response.redirect(self.context.absolute_url())
        return ''
