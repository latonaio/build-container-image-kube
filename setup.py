# coding: utf-8

# Copyright (c) 2019-2020 Latona. All rights reserved.

from setuptools import setup, find_packages

setup(
    name="build-container-image",
    version="0.0.1",
    author="XXXXXX",
    packages=find_packages("./src"),
    package_dir={"":"src"},
    install_requires=[
        "dockerfile-parse",
        "setuptools",
        "GitPython",
        "requests==2.21.0",
        "urllib3==1.24.2",
        "chardet==3.0.4",
        "pathlib",
        "pycurl"
    ],
    tests_require=[]
)
