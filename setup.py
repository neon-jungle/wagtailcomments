#!/usr/bin/env python
"""
Install Wagtail Comments using setuptools
"""

from setuptools import find_packages, setup

with open('README.rst', 'r') as f:
    readme = f.read()

with open('wagtailcomments/_version.py', 'r') as f:
    version = None
    exec(f.read())

setup(
    name='wagtailcomments',
    version=version,
    description="",
    long_description=readme,
    author='Takeflight',
    author_email='tim@takeflight.com.au',
    url='https://github.com/takeflight/wagtailcomments',

    install_requires=[
        'Django>=1.9',
        'wagtail>=1.5',
        'django-enumchoicefield>=0.5.2',
        'django-ipware',
    ],
    zip_safe=False,
    license='BSD License',

    packages=find_packages(),

    include_package_data=True,
    package_data={},

    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Framework :: Django',
        'License :: OSI Approved :: BSD License',
    ],
)
