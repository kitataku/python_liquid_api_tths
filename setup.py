from setuptools import setup
import python_liquid_api


NAME = "python_liquid_api_tths"
AUTHOR = "kitataku"
EMAIL = ""
MAINTAINER = "kitataku"
MAIN_EMAIL = ""
DESCRIPTION = "Use Liquid API with Python"
LICENSE = "MIT License"
URL = "https://github.com/kitataku/python_liquid_api_tths"
VERSION = python_liquid_api.__version__
PYTHON_REQUIRES = ">=3.6"

INSTALL_REQUIRES = [
    "PyJWT>=2.1.0",
    "pandas>=1.3.4",
    "numpy>=1.20.3",
]

PACKAGES = [
    "python_liquid_api"
]

with open("README.md", "r") as f:
    readme = f.read()

long_description = readme
