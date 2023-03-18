# coding: utf-8

from os import path

from setuptools import setup, find_packages


HERE = path.abspath(path.dirname(__file__))

try:
    # Get the long description from the README file
    with open(path.join(HERE, "README.md"), encoding="utf-8") as f:
        long_description = f.read()
except IOError:
    long_description = "README file unavailable"


setup(
    name="bachelor_core",
    version="0.0.1",
    packages=find_packages(exclude=["docs", "tests"]),
    install_requires=["setuptools", "flask"],
    python_requires=">=3.0, <4",
    author="Ivanenko Grigoriy",
    long_description=long_description,
    long_description_content_type="text/markdown",
)
