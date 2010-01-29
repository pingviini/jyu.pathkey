# -*- coding: utf-8 -*-

from zope.interface import Interface
from zope.interface import Attribute
from zope import schema
from zope.component.interfaces import IObjectEvent
from jyu.pathkey import _


class IPathkeyControlPanelForm(Interface):
    """ Pathkey control panel """


class IPathkeyFinnishForm(Interface):
    """ Finnish pathkey content """
    
    pathkeyTitle_fi = schema.TextLine(
        title = _(u"Legend text"),
        description = _(u"You can give custom legend text"),
        required = False,
        default = u"Polkuavain",
    )

    pathkeyDescription_fi = schema.SourceText(
        title = _(u"Additional description for pathkey requester form"),
        required = False,
        default = u"Sisällön omistaja on estänyt pääsyn sisältöön. Anna oikea polkuavain jatkaaksesi.",
    )


class IPathkeyEnglishForm(Interface):
    """ English pathkey content """
    
    pathkeyTitle_en = schema.TextLine(
        title = _(u"Legend text"),
        description = _(u"You can give custom legend text"),
        required = False,
        default = u"Pathkey",
    )

    pathkeyDescription_en = schema.SourceText(
        title = _(u"Additional description for pathkey requester form"),
        required = False,
        default = u"Access restricted by contents owner. Please give correct pathkey to continue.",
    )


class IPathkeyListing(Interface):
    """ Lists all pathkeys """

    
class IPathkey(IPathkeyFinnishForm, IPathkeyEnglishForm, IPathkeyListing):
    """ A marker class for pathkey """

class IAfterTraverseEvent(IObjectEvent):
    """An event which gets sent on publication traverse completion"""

    request = Attribute("The current request")
