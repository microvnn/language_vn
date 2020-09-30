#!/usr/bin/env python
# -*- coding: utf-8 -*-
import io
import os
from setuptools import setup

install_requires = [
    "Click>=6.0",
    "python-crfsuite==0.9.6",
    "nltk>=3.4,<3.5",
    "unidecode",
]

setup_requires = []

setup(
    name="language_vn",
    version="1.0.0",
    description="Vietnamese NLP Toolkit",
    author="hungth",
    author_email="microvnn@gmail.com",
    url="https://github.com/microvnn/language_vn",
    packages=["language_vn",],
    package_dir={"language_vn": "language_vn"},
    entry_points={"console_scripts": ["language_vn=language_vn.cli:main"]},
    include_package_data=True,
    install_requires=install_requires,
    license="GNU General Public License v3",
    zip_safe=False,
    keywords="language_vn",
    classifiers=[
        "Development Status :: 1 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Natural Language :: Vietnamese",
        "Programming Language :: Python :: 3.6",
    ],
)
