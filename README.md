DoorstopDemo
============

[![Build Status](https://travis-ci.org/jacebrowning/doorstop-demo.png?branch=master)](https://travis-ci.org/jacebrowning/doorstop-demo)
[![Coverage Status](https://coveralls.io/repos/jacebrowning/doorstop-demo/badge.png?branch=master)](https://coveralls.io/r/jacebrowning/doorstop-demo?branch=master)

[![Wercker Status](https://app.wercker.com/status/25748caabe06f84fe4ec2c9866b04a50/m/ "Wercker Status")](https://app.wercker.com/project/bykey/25748caabe06f84fe4ec2c9866b04a50)

This is a copy of Doorstop using random requirements as a demonstration.


Getting Started
===============

Requirements
------------

-   Python 3.3
-   A version control system for requirements storage


Installation
------------

DoorstopDemo can be installed in a virtualenv from source:

    $ git clone https://github.com/jacebrowning/doorstop-demo.git
    $ cd doorstop-demo
    $ make



Basic Usage
===========

To generate new random requirements:

    $ make random

To validate the requirements:

    $ make doorstop

To generate HTML:

    $ make html

To open the generated HTML in a browser:

    $ make read
