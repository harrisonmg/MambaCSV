#!/usr/bin/env python

from distutils.core import setup

setup(
    name='mambaplot',
    version='0.0.0',
    description='Quick CSV Plotting Utility',
    author='Harrison Gieraltowski',
    author_email='gieraltowski.har@gmail.com',
    url='https://www.harrisonmg.net/mambaplot/',
    entry_points={
        'console_scripts': [
            'mambaplot = mambaplot:main'
        ]
    }
)
