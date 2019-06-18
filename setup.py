# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open("README.md") as f:
    readme = f.read()

setup(
    name = "ArduinoScope",
    version = "0.0.1",
    description = "A oscilloscope for using arduino board.",
    long_description = readme,
    #  packages = ["ArduinoScope" ],
    packages = find_packages(),
    package_data = {},
    install_requires = [ ],
    author = "Dilawar Singh",
    author_email = "dilawars@ncbs.res.in",
    url = "http://github.com/dilawar/ArduinoScope",
    license='GPL',
)
