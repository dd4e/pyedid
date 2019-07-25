"""
Setup module
"""
from os import path

from setuptools import setup, find_packages

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="pyedid",
    version="0.1",
    packages=find_packages(),
    entry_points={"console_scripts": ["pyedid = pyedid.main:main"]},
    author="Jonas Lieb",
    author_email="",
    maintainer="Davydov Denis",
    maintainer_email="dadmoscow@gmail.com",
    url="https://github.com/dadmoscow/pyedid",
    description="This is a python library to parse extended display identification data (EDID)",
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords="edid xrandr display",
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries",
        "Topic :: System :: Hardware",
    ]
)
