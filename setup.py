from setuptools import setup
import python_liquid_api


NAME = "python_liquid_api_tths"
AUTHOR = "kitataku"
EMAIL = ""
DESCRIPTION = "Use Liquid API with Python"
CONTENT_TYPE = "text/markdown"
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

setup(
    name=NAME,
    author=AUTHOR,
    author_email=EMAIL,
    maintainer=AUTHOR,
    maintainer_email=EMAIL,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type=CONTENT_TYPE,
    licence=LICENSE,
    url=URL,
    version=VERSION,
    python_requires=PYTHON_REQUIRES,
    install_requires=INSTALL_REQUIRES,
    packages=PACKAGES
)
