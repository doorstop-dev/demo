#!/usr/bin/env python

"""
Setup script for DoorstopDemo.
"""

import setuptools

from demo import __project__, __version__, CLI, GUI

import os
if os.path.exists('README.rst'):
    README = open('README.rst').read()
else:
    README = ""  # a placeholder, readme is generated on release
CHANGES = open('CHANGES.md').read()

setuptools.setup(
    name=__project__,
    version=__version__,

    description="A sample Doorstop project using random requirements.",
    url='http://github.com/jacebrowning/doorstop-demo',
    author='Jace Browning',
    author_email='jacebrowning@gmail.com',

    packages=setuptools.find_packages(),
    package_data={'demo.core': ['files/*']},

    entry_points={'console_scripts': [CLI + ' = demo.cli.main:main',
                                      GUI + ' = demo.gui.main:main']},

    long_description=(README + '\n' + CHANGES),
    license='LGPL',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Console',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',  # pylint: disable=C0301
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.3',
        'Topic :: Software Development :: Documentation',
        'Topic :: Text Editors :: Documentation',
        'Topic :: Text Processing :: Markup',
    ],

    install_requires=["PyYAML == 5.1", "Markdown == 2.3.1", "requests"],
)
