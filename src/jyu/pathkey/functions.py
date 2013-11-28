# -*- coding: utf-8 -*-

import md5
try:
    from urlparse import parse_qs
except ImportError:  # old version, grab it from cgi
    from cgi import parse_qs


def fullRequestUrlFrom(request):
    if request.QUERY_STRING:
        return request.URL + "?" + request.QUERY_STRING
    return request.URL


def redirectUrlFrom(request):
    qs = parse_qs(request.QUERY_STRING)
    try:
        return qs['original_url'][0]
    except (KeyError, IndexError):
        return None


def getMD5SUM(text, type='folder'):
    """
    Return the md5sum of the text string passed to,
    the function.
    Keyword arguments:
        text - the string from which we want to create md5sum
        type - type of the object we want to create/check. defaults to 'folder'
    """
    # type is to prevent md5 collision from the very unlikely scenario where a folder
    # is created that has the same name than the link to Korppi or www-page.
    return md5.new((type + text).encode('utf8')).hexdigest()


def unlockPathkey(request, pathkey):
    """Function for unlocking pathkey for next request"""
    pathkey = getMD5SUM(pathkey)
    request.RESPONSE.setCookie('path_key', pathkey, path='/')
