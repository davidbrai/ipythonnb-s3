#!/usr/bin/env python
from setuptools import setup


setup(
    name='s3nbmanager',
    version='0.0.1',
    description='IPython notebook manager which saves to S3',
    py_modules=['s3nbmanager'],
    url='https://github.com/davidbrai/ipythonnb-s3',
    classifiers=[
        'Programming Language :: Python',
        'Topic :: Internet :: API',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    install_requires=[
        'tornado',
        'boto',
        'ipython'
    ],
    zip_safe=False
)
