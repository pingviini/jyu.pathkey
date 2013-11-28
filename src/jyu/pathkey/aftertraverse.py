# -*- coding: utf-8 -*-
import urllib

from jyu.pathkey.functions import fullRequestUrlFrom, getMD5SUM
from jyu.pathkey.interfaces import IAfterTraverseEvent
from zope.interface import implements


from zope.component import adapter
from ZPublisher.interfaces import IPubBeforeCommit
import logging

logger = logging.getLogger("LogRequest")

@adapter(IPubBeforeCommit)
def pathkey_request_body_cleanup(event):
    request = event.request
    response = request.response

    try:
        if request.pathkey and not request.get('path_key', None):
            if not 'pathkey-requester' in request.getURL():
                response.body = ""
                response.setHeader("Content-length", 0)
    except AttributeError:
        pass


class AfterTraverseEvent(object):
    """An event which gets sent on publication traverse completion"""

    implements(IAfterTraverseEvent)

    def __init__(self, obj, request):
        self.object = obj
        self.request = request

        if not self.validatePathkey():
            qs = {}

            original_url = fullRequestUrlFrom(request)
            if original_url:
                qs['original_url'] = original_url

            if original_url and "@@embed" in original_url:
                qs['plone_skin'] = "Plain Skin"


            pathkey_request_url = "%s/%s?%s" % (
                self.object.absolute_url(),
                'pathkey-requester',
                urllib.urlencode(qs))

            self.request.response.redirect(pathkey_request_url)

    def validatePathkey(self):
        """
        Returns True if when user can access pathkey protected object.
        Returns always True if object does not have pathkey protection.
        """

        if hasattr(self.object, 'path_key'):
            pk = getattr(self.object, 'path_key')
            given_pk = self.request.get('path_key', '')
            pk = getMD5SUM(pk)
            return given_pk == pk

        # No pathkey is set, so pathkey is correct always
        return True
