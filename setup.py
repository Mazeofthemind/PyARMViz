#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""A setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages

# To use a consistent encoding
from codecs import open
from os import path
from PyARMViz import __version__

VERSION = __version__

here = path.abspath(path.dirname(__file__))


def read(fname):
    return open(path.join(here, fname)).read()


setup(
    name="PyARMViz",
    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version=VERSION,
    description="Advanced Python Association Rule Visualization Library",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    # The project's main homepage.
    url="",
    # Author details
    author="caleb",
    author_email="caleb.wharton@gmail.com",
    # Choose your license
    license="MIT",
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 3 - Alpha",
        # Indicate who your project is intended for
        # 'Intended Audience :: End Users/Desktop',
        # 'Intended Audience :: Healthcare Industry',
        # Pick your license as you wish (should match "license" above)
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(".", exclude=["contrib", "docs", "tests"]),
    package_dir={"PyARMViz": "PyARMViz"},
    
    #Must be manually updated to include non-Python files during install
    #Note the MANIFEST.in file may not be required
    package_data={'PyARMViz/datasets': ['*.json', '*.tar.xz']},
    
    # Alternatively, if you want to distribute just a my_module.py, uncomment
    # this:
    #   py_modules=["my_module"],
    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=[
        "plotly",
        "networkx",
        "numpy"
        ],
    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    # extras_require={
    #     'dev': ['check-manifest'],
    #     'test': ['coverage'],
    # },
)
