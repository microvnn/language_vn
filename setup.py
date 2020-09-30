#!/usr/bin/env python
# -*- coding: utf-8 -*-
import io
import os
from setuptools import setup

# Use the VERSION file to get version
version_file = os.path.join(os.path.dirname(__file__), "language_vn", "VERSION")
with open(version_file) as fh:
    version = fh.read().strip()

install_requires = [
    "python-crfsuite==0.9.6",
    "nltk>=3.4",
    "unidecode",
    "pickle",
]

setup_requires = []

setup(
    name="language_vn",
    version=version,
    description="Vietnamese NLP Toolkit",
    author="Hungth",
    author_email="microvnn@gmail.com",
    url="https://github.com/undertheseanlp/underthesea",
    packages=["underthesea",],
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
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.6",
    ],
    setup_requires=setup_requires,
)
