#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('requirements.txt') as req_file:
    requirements = req_file.read().split('\n')

with open('requirements-dev.txt') as req_file:
    requirements_dev = req_file.read().split('\n')

with open('VERSION') as fp:
    version = fp.read().strip()

setup(
    name='mcshell',
    version=version,
    description="This is the mcshell project.",
    long_description=readme,
    author="Simon de Haan",
    author_email='simon@praekeltfoundation.org',
    url='https://github.com/smn/mcshell',
    packages=[
        'mcshell',
    ],
    package_dir={'mcshell':
                 'mcshell'},
    include_package_data=True,
    install_requires=requirements,
    license="BSD",
    zip_safe=False,
    keywords='mcshell',
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
    ]
)
