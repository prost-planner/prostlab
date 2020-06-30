#! /usr/bin/env python

from setuptools import setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="prostlab",
    version="1.0",
    description="Perform experiments with the Prost planner",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="experiment lab Prost",
    author="Thomas Keller",
    author_email="thomaskeller79@gmail.com",
    url="https://github.com/prost-planner/prostlab",
    license="GPL3+",
    packages=["prostlab", "prostlab.parsers", "prostlab.reports"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering",
    ],
    install_requires=["lab==6.0",],
    python_requires=">=3.6",
)
