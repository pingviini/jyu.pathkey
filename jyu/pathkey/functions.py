import md5

def getMD5SUM(text,type='folder'):
    """
    Return the md5sum of the text string passed to,
    the function.
    Keyword arguments:
        text - the string from which we want to create md5sum
        type - type of the object we want to create/check. defaults to 'folder'
    """
    # type is to prevent md5 collision from the very unlikely scenario where a folder
    # is created that has the same name than the link to Korppi or www-page.
    return md5.new( (type+text).encode('utf8')).hexdigest()

