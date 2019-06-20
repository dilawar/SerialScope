# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open("README.md") as f:
    readme = f.read()
# 

setup(
    name = "SerialScope",
    version = "0.0.3",
    description = "A serial-port based oscilloscope",
    long_description = readme,
    long_description_content_type='text/markdown',
    packages = find_packages(),
    package_data = {},
    install_requires = ['PySimpleGUI', 'screeninfo', 'pyserial'],
    author = "Dilawar Singh",
    author_email = "dilawars@ncbs.res.in",
    url = "http://github.com/dilawar/SerialScope",
    license='GPLv3',
    entry_points = {
        'console_scripts' : [ 
            'serialscope = SerialScope.__main__:main'
            ],
        }
)
