import os
import sfdxmagic

from setuptools import setup
from sfdxmagic import __version__

version = sfdxmagic.__version__

description = open(
    os.path.join(os.path.abspath(os.path.dirname(__file__)), "README.md")
).read()

dependencies = ["jupyterlab", "pandas"]


setup(
    name="sfdxmagic",
    py_modules=["sfdxmagic"],
    version=version,
    description="Execute cells with SOQL and APEX within Jupyter notebooks",
    long_description=description,
    author="Daniele Piccone",
    author_email="mild.taste@gmail.com",
    keywords=["soql", "jupyter", "salesforce", "apex"],
    install_requires=dependencies,
)
