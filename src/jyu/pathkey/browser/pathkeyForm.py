# -*- coding: utf-8 -*-
# Five package has changed place in Plone 4.1
try:
    # Plone 4.1
    from five.formlib.formbase import PageForm
except ImportError:
    # Oldies
    from Products.Five.formlib.formbase import PageForm

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.statusmessages.interfaces import IStatusMessage
from zope.formlib import form
from zope.formlib.form import setUpWidgets
from zope.interface import Interface, invariant
from zope.interface import alsoProvides, noLongerProvides
from zope.schema import Password, Bool, TextLine
from zope.schema import ValidationError

from jyu.pathkey.functions import (
    unlockPathkey,
    fullRequestUrlFrom,
    redirectUrlFrom
)
from jyu.pathkey.interfaces import IPathkey
from jyu.pathkey import _


class AllFieldsRequired(ValidationError):
    __doc__ = _("""Required input is missing.""")


class IPathkeyForm(Interface):
    """
    Pathkeyform schema
    """

    path_key = TextLine(
        title=_(u'Pathkey'),
        description=_(u'If you want to protect contents of this folder, set a pathkey.'),
        required=False,)

    pathkey_owner = TextLine(
        title=_(u"Pathkey owner"),
        description=_(u"Name of the person who knows the pathkey."),
        required=False,)

    pathkey_owner_email = TextLine(
        title=_(u"Pathkey owners email"),
        description=_(u"This will be visible so that users know where to ask correct pathkey."),
        required=False,)

    reset_pathkey = Bool(
        title=_(u'Delete pathkey'),
        description=_(u'Deletes the pathkey from this item after sending the form.'),
        required=False,)

    @invariant
    def othersFilled(data):
        fields = {'path_key': data.path_key,
                  'pathkey_owner': data.pathkey_owner,
                  'pathkey_owner_email': data.pathkey_owner_email}
        if data.reset_pathkey:
            pass
        elif not (data.path_key and data.pathkey_owner and data.pathkey_owner_email):
            for field in fields.keys():
                if fields[field]:
                    del(fields[field])

            missing = tuple(fields)  # + (('All fields are required',),)

            raise AllFieldsRequired(missing)


class PathkeyForm(PageForm):
    """
    Pathkey form
    """
    template = ViewPageTemplateFile('set_pathkey.pt')
    form_fields = form.Fields(IPathkeyForm)

    def __init__(self, context, request):
        """ set up a few convenience object attributes """

        self.context, self.request = context, request
        self.response = self.request.RESPONSE

    # Below we process the form with action_send form handler.
    # First we check if there is already an existing path key
    # and if there is we'll set a new path key. If path_key
    # property doesn't exist in context we'll create it.

    def deletePathkey(self):
        self.context.manage_delProperties(['path_key'])
        try:
            self.context.manage_delProperties(['pathkey_owner'])
            self.context.manage_delProperties(['pathkey_owner_email'])
        except:
            # There is a chance we don't have owner and email properties set.
            pass

        noLongerProvides(self.context, IPathkey)

    def setPathkeyInfo(self, pathkey, owner, email, modify=False):
        if modify:
            self.context.manage_changeProperties({'path_key': pathkey})
            try:
                bool(self.context.pathkey_owner)
                self.context.manage_changeProperties({'pathkey_owner': unicode(owner)})
                self.context.manage_changeProperties({'pathkey_owner_email': email})
            except AttributeError:
                self.context.manage_addProperty('pathkey_owner', unicode(owner), 'string')
                self.context.manage_addProperty('pathkey_owner_email', email, 'string')
        else:
            self.context.manage_addProperty('path_key', pathkey, 'string')
            self.context.manage_addProperty('pathkey_owner', unicode(owner), 'string')
            self.context.manage_addProperty('pathkey_owner_email', email, 'string')

    @form.action("send")
    def action_send(self, action, data):

        status = IStatusMessage(self.request)
        new_pathkey = data['path_key']
        delete_enabled = data['reset_pathkey']
        new_pathkey_owner = data['pathkey_owner']
        new_pathkey_owner_email = data['pathkey_owner_email']

        try:
            old_pathkey = self.context.path_key
        except:
            old_pathkey = None

        if delete_enabled:
            self.deletePathkey()
            status.addStatusMessage(_(u"Succesfully deleted the pathkey."))

        elif old_pathkey:
            if not new_pathkey:
                self.deletePathkey()
                status.addStatusMessage(_(u"Succesfully deleted the pathkey and related information."))

            elif new_pathkey:
                self.setPathkeyInfo(new_pathkey, new_pathkey_owner, new_pathkey_owner_email, modify=True)
                status.addStatusMessage(_("Modification of the pathkey succeeded."))

        else:
            if new_pathkey:
                self.setPathkeyInfo(new_pathkey, new_pathkey_owner, new_pathkey_owner_email)
                alsoProvides(self.context, IPathkey)
                status.addStatusMessage(_("Added a new pathkey and related information about pathkey owner."))

        self.context.reindexObject(idxs=['object_provides'])
        self.response.redirect(self.context.absolute_url())

        return ''

    def getPathkeyContextFromAcquisitionChain(self):
        for obj in self.context.aq_chain[1:-1]:
            if getattr(obj.aq_base, 'path_key', None):
                return obj.absolute_url()
        return None

    def getValuesForSetPathkeyForm(self):
        """ Returns pathkey values as dict """
        try:
            pathkey_owner = unicode(getattr(self.context.aq_base, 'pathkey_owner', ''),
                                    encoding='utf-8', errors='ignore')
        except TypeError:
            pathkey_owner = getattr(self.context.aq_base, 'pathkey_owner', '')

        data = {'path_key': getattr(self.context.aq_base, 'path_key', None),
                'pathkey_owner': pathkey_owner,
                'pathkey_owner_email': getattr(self.context.aq_base, 'pathkey_owner_email', None)}

        return data

    def setUpWidgets(self, ignore_request=False):
        """From zope.formlib.form.Formbase.

        Difference: pass extra data=self.request.form.
        """
        data = self.getValuesForSetPathkeyForm()

        self.adapters = {}
        self.widgets = setUpWidgets(
            self.form_fields, self.prefix, self.context, self.request,
            form=self, adapters=self.adapters, ignore_request=ignore_request,
            data=data)

    def update(self):
        super(PathkeyForm, self).update()

        for widget in self.widgets:
            name = widget.context.getName()
            for error in self.errors:
                if name in error.args:
                    widget._error = error


class IPathkeyCheck(Interface):
    """Pathkey requester interface"""

    pathkey = Password(title=_(u"Enter the pathkey"))


class PathkeyRequest(PageForm):
    """Pathkey requester view"""

    template = ViewPageTemplateFile('pathkey_requester.pt')
    form_fields = form.Fields(IPathkeyCheck)

    def getOriginalURL(self):
        """docstring for fname"""
        return fullRequestUrlFrom(self.request)

    def getContentTitle(self):
        return self.context.Title()

    def __init__(self, context, request):
        """ set up a few convenience object attributes """

        self.context = context
        self.request = request
        self.response = self.request.RESPONSE
        self.settings = self.context.portal_pathkey
        self.language = self.request.get('LANGUAGE', 'fi')

        # IE does not allow setting cookies in iframes by default. This should
        # fix it. More info:
        # http://stackoverflow.com/questions/389456/cookie-blocked-not-saved-in-iframe-in-internet-explorer/2297382#2297382
        self.request.response.headers['P3P'] = 'CP="NOI ADM DEV COM NAV OUR STP"'

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

    def checkPermissions(self):
        """ Returns true if user has permission to view content """

        user = self.request.get('AUTHENTICATED_USER', None)
        if user:
            return user.has_permission('Modify portal content', self.context)
        return False

    def hasOwnerAndEmail(self):
        try:
            if self.context.pathkey_owner and self.context.pathkey_owner_email:
                return True
            else:
                return False
        except:
            return False

    @form.action("send")
    def action_send(self, action, data):

        try:
            suggested_pathkey = data['pathkey']
        except KeyError:
            suggested_pathkey = False

        if suggested_pathkey:
            unlockPathkey(self.request, suggested_pathkey)

        self.response.redirect(redirectUrlFrom(self.request)
                               or self.context.absolute_url())

        return ''
