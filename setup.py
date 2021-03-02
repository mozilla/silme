from setuptools import setup, find_packages
import sys
import os.path

"""Python localization library

New library for localization written in Python.
"""

docstrings = __doc__.split("\n")

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "lib"))

import silme  # noqa: E402

classifiers = """\
Development Status :: 4 - Beta
Intended Audience :: Developers
License :: OSI Approved :: GNU General Public License (GPL)
License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)
License :: OSI Approved :: Mozilla Public License 1.1 (MPL 1.1)
Operating System :: OS Independent
Programming Language :: Python :: 3.6
Programming Language :: Python :: 3.7
Programming Language :: Python :: 3.8
Programming Language :: Python :: 3.9
Topic :: Software Development :: Libraries :: Python Modules
Topic :: Software Development :: Localization
"""

setup(
    name="silme",
    version=silme.get_short_version(),
    author="Zbigniew Braniecki",
    author_email="gandalf@mozilla.com",
    description=docstrings[0],
    long_description="\n".join(docstrings[2:]),
    license="MPL 1.1/GPL 2.0/LGPL 2.1",
    url="https://github.com/mathjazz/silme",
    classifiers=filter(None, classifiers.split("\n")),
    platforms=["any"],
    package_dir={"": "lib"},
    packages=find_packages("lib"),
    keywords="localization, l10n",
)
