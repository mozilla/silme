"""Python localization library 

New library for localization written in Python.
"""

docstrings = __doc__.split("\n")

import ez_setup
ez_setup.use_setuptools()

from setuptools import setup, find_packages
import sys
import os.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lib'))

import silme

classifiers = """\
Development Status :: 4 - Beta
Intended Audience :: Developers
License :: OSI Approved :: GNU General Public License (GPL)
License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)
License :: OSI Approved :: Mozilla Public License 1.1 (MPL 1.1)
Operating System :: OS Independent
Programming Language :: Python :: 2.5
Programming Language :: Python :: 2.6
Topic :: Software Development :: Libraries :: Python Modules
Topic :: Software Development :: Localization
"""

from setuptools import Command
import glob

setup(name="silme",
      version=silme.get_short_version(),
      author="Zbigniew Braniecki",
      author_email="gandalf@mozilla.com",
      description=docstrings[0],
      long_description="\n".join(docstrings[2:]),
      license="MPL 1.1/GPL 2.0/LGPL 2.1",
      url = "http://hg.mozilla.org/l10n/silme/",
      classifiers=filter(None, classifiers.split("\n")),
      platforms=["any"],
      package_dir={'': 'lib'},
      packages = find_packages('lib'),
      keywords = "localization, l10n, l20n"
      )
