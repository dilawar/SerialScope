# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open("README.md") as f:
    readme = f.read()

setup(
    name = "SerialScope",
    version = "0.0.1",
    description = "A serial-port based oscilloscope",
    long_description = readme,
    packages = find_packages(),
    package_data = {},
    install_requires = [ ],
    author = "Dilawar Singh",
    author_email = "dilawars@ncbs.res.in",
    url = "http://github.com/dilawar/SerialScope",
    license='GPL',
)