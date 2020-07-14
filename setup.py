#!/usr/bin/env python
# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os
import re

import setuptools

ROOT = os.path.abspath(os.path.dirname(__file__))
UTF8 = 'utf8'

with open(os.path.join(ROOT, 'README.md'), mode='rt', encoding=UTF8) as fp:
    README = fp.read()

with open(os.path.join(ROOT, 'sections/__init__.py'), mode='rt', encoding=UTF8) as fp: # yapf:disable
    VERSION = re.search(r'__version__ = \'(.*?)\'', fp.read()).group(1)

with open(os.path.join(ROOT, "requirements.txt"), mode='rt', encoding=UTF8) as fp: # yapf:disable
    INSTALL = [line for line in fp.readlines() if line and '#' not in line]

if __name__ == "__main__":
    # allow setup.py to run from another directory
    os.chdir(ROOT)
    setuptools.setup(
        author='Helmut Konrad Fahrendholz',
        author_email='info@checkitweg.de',
        description='i need some trust',
        include_package_data=True,
        install_requires=INSTALL,
        long_description=README,
        name='sections',
        platforms='any',
        url='https://dev.package.checkitweg.de/sections',
        version=VERSION,
        zip_safe=False,  # create 'zip'-file if True. Don't do it!
        classifiers=[
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
        ],
        packages=[
            'sections',
            'sections.feature',
            'sections.utils',
            'sections.workplan',
        ],
        entry_points={
            'console_scripts': ['sections = sections.cli:main'],
        },
    )
