from jyu.pathkey.functions import getMD5SUM
from jyu.pathkey.interfaces import IAfterTraverseEvent
from zope.interface import implements

class AfterTraverseEvent(object):
    """An event which gets sent on publication traverse completion"""

    implements(IAfterTraverseEvent)

    def __init__(self, obj, request):
        self.object = obj
        self.request = request

        if hasattr(self.object, 'path_key'):
            pk = getattr(self.object, 'path_key')
            given_pk = request.get('path_key', '')
            pk = getMD5SUM(pk)
            if given_pk != pk:
                self.request.response.redirect(self.object.absolute_url()+'/pathkey-requester')