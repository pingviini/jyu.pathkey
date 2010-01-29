# -*- coding: utf-8 -*-

import sys

from AccessControl import ClassSecurityInfo
from Acquisition import aq_parent
from Products.CMFCore.interfaces import IDublinCore

from zope.event import notify
from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty
from zope.component import getUtility
from zope.interface import classProvides

from jyu.pathkey.aftertraverse import AfterTraverseEvent
from jyu.pathkey.interfaces import IPathkey
from jyu.pathkey.interfaces import IPathkeyFinnishForm
from jyu.pathkey.interfaces import IPathkeyEnglishForm
from jyu.pathkey.interfaces import IPathkeyListing

from OFS.SimpleItem import SimpleItem


def postTraversehook():
    """
    This hook will be called when traversal is complete
    """

    frame = sys._getframe(2)
    published = frame.f_locals['object']

    # If we're goin to pathkey-requester form we'll skip this hook
    if 'pathkey-requester' in published.__name__:
        return

    # obj in here might be the template so we need to get it's parent.
    # It might also be objects method (Images, Files) - for which aq_parent
    # throws AttributeError. We'll handle this in except clause.
    try:
        obj = published.aq_parent
    except AttributeError:
        obj = published.im_self
    
    request = frame.f_locals['self']
    
    if IDublinCore.providedBy(obj) and hasattr(obj, 'path_key'):
        notify(AfterTraverseEvent(obj, request))


def insertPostTraversalHook(object, event):
    """
    Hook into the request.post_traversal through the IBeforeTraverse event
    only registered for ISiteRoot.
    """
    event.request.post_traverse(postTraversehook)

    
def form_adapter(context):
    """Form Adapter"""
    return getUtility(IPathkey)


class Pathkey(SimpleItem):
    """Pathkey Utility"""
    implements(IPathkey)

    classProvides(
        IPathkeyFinnishForm,
        IPathkeyEnglishForm,
        IPathkeyListing,
        )

    security = ClassSecurityInfo()

    pathkeyTitle_fi = FieldProperty(IPathkeyFinnishForm['pathkeyTitle_fi'])
    pathkeyDescription_fi = FieldProperty(IPathkeyFinnishForm['pathkeyDescription_fi'])

    pathkeyTitle_en = FieldProperty(IPathkeyEnglishForm['pathkeyTitle_en'])
    pathkeyDescription_en = FieldProperty(IPathkeyEnglishForm['pathkeyDescription_en'])
