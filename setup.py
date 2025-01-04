#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pathlib
import re

from setuptools import find_packages, setup


def read_text(*fnames):
    return pathlib.Path(__file__).parent.joinpath(*fnames).read_text()


def get_requirements(basename):
    return read_text("requirements", f"{basename}.txt").strip().split("\n")


version = re.search(
    r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
    read_text("bor", "__init__.py"),
    re.MULTILINE,
).group(1)

if not version:
    raise RuntimeError("Cannot find version information")

extras_require = {key: get_requirements(key) for key in ["dev", "test"]}

setup(
    name="bor-tools",
    version=version,
    description="Small Python library to manipulate BOR files",
    keywords="bor",
    long_description=read_text("README.rst") + "\n\n" + read_text("CHANGES.rst"),
    url="https://github.com/LIMSAS/bor-file",
    author="Salem Harrache",
    author_email="dev@mail.lim.eu",
    package_dir={"bor": "bor"},
    packages=find_packages(),
    include_package_data=True,
    license="MIT license",
    zip_safe=False,
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    install_requires=get_requirements("base"),
    extras_require=extras_require,
)
