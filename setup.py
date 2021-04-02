'''Setup module'''
import os
from setuptools import setup, find_packages

def read(rel_path: str) -> str:
    here = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()

def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]

long_description = read('README.md')
version = get_version('pyedid/__init__.py')


setup(
    name='pyedid',
    version=version,
    packages=find_packages(exclude=['tests']),
    author='Davydov Denis, Jonas Lieb',
    author_email='dadmoscow@gmail.com',
    url='https://github.com/dd4e/pyedid',
    description='Library to parse extended display identification data (EDID)',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT',
    install_requires=[
        "requests>=2"
    ],
    keywords=[
        'edid',
        'xrandr',
        'display',
        'monitor',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development :: Libraries',
        'Topic :: System :: Hardware',
    ]
)
