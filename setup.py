import ez_setup
ez_setup.use_setuptools()

import os
import sys
from setuptools import setup

version_py = os.path.join(os.path.dirname(__file__), 'entabled', 'version.py')
version = open(version_py).read().strip().split('=')[-1].replace('"','')

long_description = """
Package for creating browser-viewable tables from data files
"""

setup(
        name="entabled",
        version=version,
        install_requires=['simplejson', 'jinja2'],
        packages=['entabled',
                  'entabled.data',
                  'entabled.scripts',
                  ],
        author="Ryan Dale",
        description=long_description,
        long_description=long_description,
        url="none",
        package_data = {'entabled':["data/*"]},
        package_dir = {"entabled": "entabled"},
        scripts = ['entabled/scripts/deseq2table.py'],
        author_email="dalerr@niddk.nih.gov",
        classifiers=['Development Status :: 4 - Beta'],
    )
