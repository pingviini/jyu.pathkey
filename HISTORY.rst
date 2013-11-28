Changelog
=========

1.7.1 (unreleased)
------------------

- Nothing changed yet.


1.7.0 (2013-10-16)
------------------

- Fix CSS to use rendering='link' instead of 'import'
  [datakurre]

1.6 (2013-09-25)
----------------

- Works with Plone 4.3

1.5.4 (2013-04-10)
------------------

- Prevented setting pathkey to folders default view.

1.5.3 (2012-03-28)
------------------

- Fixed permissions

1.5.2 (2012-02-02)
------------------

- Removed title from css registration.

1.5.1 (2011-10-17)
------------------

-  Minimal fix to make pathkey work with plone.app.theming and filesystem
   resources

1.5 (2011-08-24)
----------------

- Add separate permission for path key managing. The permission is given to
  Owner, Manager, Editor and Contributor by default.

1.4 (2011-03-31)
----------------

- Clears response body and sets Content-Length to 0 when redirecting to
  pathkey-requester view.

1.3 (2011-02-07)
----------------

- Separate pathkey detection and unlocking to own functions [epeli].
- Remember the exact url where user where going [epeli].
- Use Plain Skin on PathkeyRequest FormPage when requested view is @@embed.
  [epeli]
- Removed commented code. [epeli]

1.1.4 (2010-03-05)
------------------

- Fixed typo in setup.py

1.1.3 (2010-03-05)
------------------

- Added z3c.autoinclude.plugin

1.1.2 (2010-02-11)
------------------

- Moved the pathkey form to object tabs instead of document actions
- Added delete pathkey checkbox

1.1.1 (2010-02-09)
------------------

- Fixed problem with dexterity content types

1.1 (2010-02-08)
----------------

- Fixed bug where opening files and images with straight url went past
  pathkey check (you still need to disable caching for files-images).
- Restructured code and views so that jyu.pathkey works with Plone 4

1.0.2 (2009-11-20)
------------------

- Fixed encoding problem with pathkey requester

1.0.1 (2009-11-18)
------------------

- Fixed missing legend text from pathkey requester template.

1.0 (2009-11-08)
----------------

- Content owner can set and remove pathkey for any content (removing happens
  by saving empty pathkey)
- Added pathkey-list view for content owner to see where pathkeys have been
  set (by owner).
- Added functional doctests
