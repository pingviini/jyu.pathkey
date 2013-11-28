# -*- coding: utf-8 -*-

from zope.interface import implements

from plone.fieldsets.fieldsets import FormFieldsets
from plone.app.controlpanel.form import ControlPanelForm

from jyu.pathkey.interfaces import IPathkeyControlPanelForm
from jyu.pathkey.interfaces import IPathkeyFinnishForm
from jyu.pathkey.interfaces import IPathkeyEnglishForm
from jyu.pathkey.interfaces import IPathkeyListing
from jyu.pathkey import _


class PathkeyControlPanelForm(ControlPanelForm):
    """ Pathkey control panel """
    implements(IPathkeyControlPanelForm)

    pathkey_finnish = FormFieldsets(IPathkeyFinnishForm)
    pathkey_finnish.id = 'pathkey_finnish'
    pathkey_finnish.label = _(u"Additional Finnish content")

    pathkey_english = FormFieldsets(IPathkeyEnglishForm)
    pathkey_english.id = 'pathkey_english'
    pathkey_english.label = _(u"Additional English content")

    pathkey_listing = FormFieldsets(IPathkeyListing)
    pathkey_listing.id = 'pathkey_listing'
    pathkey_listing.label = _(u"List all pathkeys")

    form_fields = FormFieldsets(pathkey_finnish, pathkey_english, pathkey_listing)

    form_name = _(u"Pathkey settings")
    label = _(u"Pathkey settings")
    description = _(u"Here you can customize the contents of the form requesting pathkey.")