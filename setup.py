import sys
from setuptools import setup, find_packages

version = '1.7.1.dev0'

install_requires = ["setuptools"]

if sys.version_info[:2] == (2, 4):
    install_requires.append("ZPublisherEventsBackport")


setup(name="jyu.pathkey",
      version=version,
      description="Restricts access to Plone content with pathkey",
      long_description="%s\n%s" % (
          open("README.rst").read(),
          open("HISTORY.rst").read()),
      classifiers=[
          "Framework :: Plone",
          "Framework :: Plone :: 3.2",
          "Framework :: Plone :: 3.3",
          "Framework :: Plone :: 4.0",
          "Framework :: Plone :: 4.1",
          "Framework :: Plone :: 4.2",
          "Framework :: Plone :: 4.3",
          "Programming Language :: Python",
          "Programming Language :: Python :: 2.4",
          "Programming Language :: Python :: 2.6",
          "Programming Language :: Python :: 2.7",
          "Topic :: Software Development :: Libraries :: Python Modules",
      ],
      keywords="jyu.pathkey pathkey restrict",
      author="Jukka Ojaniemi",
      author_email="jukka.ojaniemi@jyu.fi",
      url="https://github.com/pingviini/jyu.pathkey",
      license="GPL",
      packages=find_packages("src", exclude=["ez_setup"]),
      package_dir={"": "src"},
      namespace_packages=["jyu"],
      include_package_data=True,
      zip_safe=False,
      install_requires=install_requires,
      extras_require={
          "test": ["plone.api",
                   "plone.app.testing",
                   "plone.app.robotframework"]},
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
