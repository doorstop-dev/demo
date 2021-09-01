DoorstopDemo
============

This is a copy of [Doorstop](https://github.com/jacebrowning/doorstop) using random requirements as a demonstration.


Getting Started
===============

Requirements
------------

- [Git](http://git-scm.com/downloads)
- [Python 3.3](https://www.python.org/download)
- [virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/#virtualenv)


Installation
------------

DoorstopDemo can be installed in a virtualenv from source:

    $ git clone https://github.com/jacebrowning/doorstop-demo.git
    $ cd doorstop-demo
    $ make env



Basic Usage
===========

To validate the requirements:

    $ make doorstop

To generate HTML:

    $ make html

To open the generated HTML in a browser:

    $ make read
    

Live Output
===========

Generated HTML:

http://doorstop-dev.github.io/demo/

Published by:

https://travis-ci.org/jacebrowning/doorstop-demo
