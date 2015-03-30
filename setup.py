#!/usr/bin/env python

from setuptools import setup

extra_opts = {}

try:
    import setuptools_markdown
except ImportError:
    pass
else:
    extra_opts = {
        "setup_requires": ['setuptools-markdown'],
        "long_description_markdown_filename": 'Readme.md'
    }

version = '0.0.4'

setup(
    name='aioli',
    packages=['aioli'],  # this must be the same as the name above
    version=version,
    description='asyncio special sauce',
    author='brettatoms',
    author_email='brettatoms@gmail.com',
    url='https://github.com/brettatoms/aioli',
    download_url='https://github.com/brettatoms/aioli/archive/master.zip',
    keywords=['aioli', 'async', 'asyncio', 'concurrency', 'concurrent'],
    classifiers=['Development Status :: 4 - Beta',
                   'Environment :: Other Environment',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: MIT License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python :: 3'],
    **extra_opts
)
