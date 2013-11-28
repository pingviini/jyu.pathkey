Introduction
============

*Jyu.pathkey* was developed to situations where users have some content in
Plone what they don't want to publish for the whole world to see, but still
want to share it with a number of people who doesn't necessarily have an user
account to the plone site. With *jyu.pathkey* contents owner can set a pathkey
for the folder/item and then share that with the people they want.

*Jyu.pathkey* is not a bullet proof solution and was never intended to be. It
simply adds user specified password (pathkey) as a new property of given folder
and adds a hook to AfterTraverseEvent to check if user is trying to access
protected content and request the pathkey when needed.

